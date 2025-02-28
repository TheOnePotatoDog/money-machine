# Safety Machine

An AI-powered risk assessment advisor that identifies potential risks and safety concerns in various scenarios.

## Features

- User authentication and profile management
- Credit-based AI query system
- Stripe integration for purchasing credits
- Risk assessment and safety advice powered by AI

## Repository Structure

```
safety-machine/
├── backend/              # FastAPI backend
│   ├── app/              # Application code
│   └── tests/            # Backend tests
├── frontend/             # React frontend
│   └── src/              # Frontend source code
└── docker-compose.yml    # Development environment setup
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker and Docker Compose (for local development)

### Setup

1. Clone this repository
2. Copy `.env.example` to `.env` and fill in your configuration
3. Run `docker-compose up` to start the development environment

## Development

See the README files in the `backend` and `frontend` directories for specific development instructions.

## License

[MIT License](LICENSE)
