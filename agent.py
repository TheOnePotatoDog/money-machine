from dataclasses import dataclass, field
import time, importlib, inspect, os, json
from typing import Any, Optional, Dict
from python.helpers import extract_tools, rate_limiter, files, errors
from python.helpers.print_style import PrintStyle
from langchain.schema import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from langchain_core.embeddings import Embeddings

@dataclass
class AgentConfig: 
    chat_model: BaseChatModel | BaseLLM
    utility_model: BaseChatModel | BaseLLM
    embeddings_model:Embeddings
    memory_subdir: str = ""
    auto_memory_count: int = 3
    auto_memory_skip: int = 2
    rate_limit_seconds: int = 60
    rate_limit_requests: int = 15
    rate_limit_input_tokens: int = 1000000
    rate_limit_output_tokens: int = 0
    msgs_keep_max: int = 25
    msgs_keep_start = 5
    msgs_keep_end = 10
    response_timeout_seconds: int = 60
    max_tool_response_length: int = 3000
    code_exec_docker_enabled: bool = True
    code_exec_docker_name: str = "agent-zero-exe"
    code_exec_docker_image: str = "frdel/agent-zero-exe:latest"
    code_exec_docker_ports: dict[str,int] = field(default_factory=lambda: {"22/tcp": 50022})
    code_exec_docker_volumes: dict[str, dict[str, str]] = field(default_factory=lambda: {files.get_abs_path("work_dir"): {"bind": "/root", "mode": "rw"}})
    code_exec_ssh_enabled: bool = True
    code_exec_ssh_addr: str = "localhost"
    code_exec_ssh_port: int = 50022
    code_exec_ssh_user: str = "root"
    code_exec_ssh_pass: str = "toor"
    additional: Dict[str, Any] = field(default_factory=dict)

class Agent:

    paused = False
    streaming_agent = None
    
    def __init__(self, number:int, config: AgentConfig):
        # agent config  
        self.config = config       

        # non-config vars
        self.number = number
        self.agent_name = f"Agent {self.number}"

        # Static system and tools prompt paths
        self.system_prompt_file = "./prompts/agent.system.md"
        self.tools_prompt = files.read_file("./prompts/agent.tools.md")

        self.history = []
        self.last_message = ""
        self.intervention_message = ""
        self.intervention_status = False
        self.rate_limiter = rate_limiter.RateLimiter(
            max_calls=self.config.rate_limit_requests,
            max_input_tokens=self.config.rate_limit_input_tokens,
            max_output_tokens=self.config.rate_limit_output_tokens,
            window_seconds=self.config.rate_limit_seconds
        )
        self.data = {}  # free data object all the tools can use

        os.chdir(files.get_abs_path("./work_dir"))  # Change CWD to work_dir
    
    def read_system_prompt(self):
        """Read the static system prompt dynamically from the file."""
        return files.read_file(self.system_prompt_file, agent_name=self.agent_name)

    def read_dynamic_prompt(self):
        """Read the dynamic prompt from the agent.dynamic.md file."""
        dynamic_prompt_path = "./prompts/agent.dynamic.md"
        return files.read_file(dynamic_prompt_path)

    def write_dynamic_prompt(self, new_content: str):
        """Write new content to the agent.dynamic.md file."""
        dynamic_prompt_path = "./prompts/agent.dynamic.md"
        with open(dynamic_prompt_path, 'w') as file:
            file.write(new_content)

    def build_full_prompt(self):
        """Build the full system prompt, including the dynamic section."""
        system_prompt = self.read_system_prompt()  # Reload system prompt from file
        dynamic_prompt_content = self.read_dynamic_prompt()  # Read dynamic prompt content
        dynamic_part = f"\n\n# Dynamic Section\n{dynamic_prompt_content}\n"
        return system_prompt + "\n\n" + self.tools_prompt + dynamic_part

    def message_loop(self, msg: str):
        """Main message loop for processing tasks."""
        try:
            printer = PrintStyle(italic=True, font_color="#b3ffd9", padding=False)
            user_message = files.read_file("./prompts/fw.user_message.md", message=msg)
            self.append_message(user_message, human=True)  # Append user's input to the history                        
            memories = self.fetch_memories(True)
            
            while True:  # Let the agent iterate on thoughts until it stops by using a tool
                Agent.streaming_agent = self  # Mark self as current streamer
                agent_response = ""
                self.intervention_status = False  # Reset intervention status

                try:
                    # Dynamically load the system prompt from the file
                    system_prompt = self.build_full_prompt()  # Include the dynamic part
                    memories = self.fetch_memories()
                    if memories:
                        system_prompt += "\n\n" + memories

                    prompt = ChatPromptTemplate.from_messages([
                        SystemMessage(content=system_prompt),
                        MessagesPlaceholder(variable_name="messages")
                    ])

                    inputs = {"messages": self.history}
                    chain = prompt | self.config.chat_model

                    formatted_inputs = prompt.format(messages=self.history)
                    tokens = int(len(formatted_inputs) / 4)
                    self.rate_limiter.limit_call_and_input(tokens)
                    
                    # Output that the agent is starting
                    PrintStyle(bold=True, font_color="green", padding=True, background_color="white").print(f"{self.agent_name}: Starting a message:")

                    for chunk in chain.stream(inputs):
                        if self.handle_intervention(agent_response): break  # Wait for intervention and handle it if paused

                        if isinstance(chunk, str):
                            content = chunk
                        elif hasattr(chunk, "content"):
                            content = str(chunk.content)
                        else:
                            content = str(chunk)
                        
                        if content:
                            printer.stream(content)  # Output the agent response stream                
                            agent_response += content  # Concatenate stream into the response

                    self.rate_limiter.set_output_tokens(int(len(agent_response) / 4))

                    if not self.handle_intervention(agent_response):
                        if self.last_message == agent_response:  # If the assistant response is the same as last message in history, let it know
                            self.append_message(agent_response)  # Append the assistant's response to the history
                            warning_msg = files.read_file("./prompts/fw.msg_repeat.md")
                            self.append_message(warning_msg, human=True)  # Append warning message to the history
                            PrintStyle(font_color="orange", padding=True).print(warning_msg)

                        else:  # Otherwise proceed with tool
                            self.append_message(agent_response)  # Append the assistant's response to the history
                            tools_result = self.process_tools(agent_response)  # Process tools requested in the agent message
                            if tools_result: return tools_result  # Break the execution if the task is done

                # Forward errors to the LLM, maybe it can fix them
                except Exception as e:
                    error_message = errors.format_error(e)
                    msg_response = files.read_file("./prompts/fw.error.md", error=error_message)  # Error message template
                    self.append_message(msg_response, human=True)
                    PrintStyle(font_color="red", padding=True).print(msg_response)
                    
        finally:
            Agent.streaming_agent = None  # Unset current streamer

    def process_tools(self, msg: str):
        """Process tools usage requests in the agent message."""
        tool_request = extract_tools.json_parse_dirty(msg)

        if tool_request is not None:
            tool_name = tool_request.get("tool_name", "")
            tool_args = tool_request.get("tool_args", {})

            tool = self.get_tool(
                        tool_name,
                        tool_args,
                        msg)
                
            if self.handle_intervention(): return  # Wait if paused and handle intervention message if needed
            tool.before_execution(**tool_args)
            if self.handle_intervention(): return  # Wait if paused and handle intervention message if needed
            response = tool.execute(**tool_args)
            if self.handle_intervention(): return  # Wait if paused and handle intervention message if needed
            tool.after_execution(response)
            if self.handle_intervention(): return  # Wait if paused and handle intervention message if needed
            if response.break_loop: return response.message
        else:
            msg = files.read_file("prompts/fw.msg_misformat.md")
            self.append_message(msg, human=True)
            PrintStyle(font_color="red", padding=True).print(msg)

    # Rest of the functions remain unchanged...
    
    