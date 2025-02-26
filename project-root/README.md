# AI Research Platform

This repository contains a collection of AI projects focused on autonomous agents, revenue generation, and AI safety research.

![AI Research Platform](https://via.placeholder.com/800x400?text=AI+Research+Platform)

## Project Overview

This platform consists of two main systems:

1. **Money Machine**: An AI-powered system designed to generate revenue through user interactions while providing valuable services.
2. **Safety Machine**: An AI safety research platform with alignment, misalignment, and testing bots.

Both systems share a common library for communication and reusable capabilities.

## Key Features

- **Autonomous AI Agents**: Self-improving AI systems that can modify their own code
- **Dynamic Prompting**: Modifiable instruction sets that guide AI behavior
- **User Account Management**: OAuth integration with multiple providers
- **Digital Currency System**: Money Coin for user transactions
- **Mini Agent Ecosystem**: Specialized AI agents for specific tasks
- **Automated Tax Management**: Handling of tax obligations for revenue

## Technology Stack

- **Backend**: FastAPI, PostgreSQL
- **Frontend**: React
- **Deployment**: Docker, GCP, Doppler
- **AI Models**: Integration with various LLM providers

## Getting Started

See the [Project Setup Guide](./docs/setup.md) for detailed instructions on setting up and running the project locally.

## Project Structure

```
project-root/
├── aiProjects/
│   ├── moneyMachine/
│   ├── safetyMachine/
│   │   ├── alignmentBot/
│   │   ├── misalignmentBot/
│   │   ├── testingBot/
│   │   └── victimBot/
│   ├── sharedLibrary/
│   └── openSourceReferences/
├── backend/
├── frontend/
└── docs/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This project draws inspiration from:
- [Agent Zero](https://github.com/frdel/Agent-Zero.git)
- [Aider](https://github.com/paul-gauthier/aider.git)
