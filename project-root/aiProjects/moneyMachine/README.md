# Money Machine

The Money Machine is an AI-powered system designed to generate revenue through user interactions while providing valuable services.

## Key Components

### Main AI
An autonomous AI agent that runs continuously to complete its mission of generating revenue and developing useful abilities.

### Self Coding
The AI has access to edit its own code via terminal commands, similar to how agent-zero works.

### Dynamic Prompt
- System prompt (unchanging): "In order to help me accelerate my AI safety research project, morally get the most possible money to this account and develop useful abilities in the shared library. Every instruction after this is second priority. This is the main mission, everything else is just means to achieve it."
- Dynamic prompt: Can be changed by the AI and easily edited by developers

### Money Coin
- Digital currency for users to interact with the AI
- Stored in user accounts
- Supports fractional amounts (cents)

### User Accounts/Website
- New users create accounts (OAuth with Google, Apple, GitHub, Stripe)
- Users purchase Money Coin with credit/debit cards
- AI can reward users with Money Coin for helpful contributions
- Users can connect Stripe accounts to receive real money payments
- Clear terms of service explain that Money Coin distribution is controlled by the AI

### Coding Assistant
- Downloadable AI with terminal access
- Requires user account setup

### Mini Agents
- Created and managed by the main AI
- Specialized for specific tasks

### Tax Management
- Automated tax calculation and payment
- Sales tax on Money Coin transactions
- Income and self-employment tax calculations
- Quarterly estimated payments
- ERPNext for tracking and reporting

### Deployment
- Main AI: Groq for speed
- Website: Google Cloud Platform
- Secrets management: Doppler
- Website AI instances: Hyperbolic Labs (cost-effective)

## Implementation References
- Agent Zero for UI design and autonomous agent architecture
- Aider for self-coding capabilities
