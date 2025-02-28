# AI Shared Library

A shared library for AI Projects containing common code and resources used by both Money Machine and Safety Machine.

## Features

- Authentication utilities
- Common database models
- Shared Pydantic schemas
- API client wrappers
- System prompts for AI agents

## Repository Structure

```
shared-library/
├── ai_shared/            # Python package with shared code
│   ├── auth.py           # Authentication utilities
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic models
│   ├── clients.py        # API client wrappers
│   └── prompts.py        # AI system prompts
└── tests/                # Tests for shared components
```

## Installation

### As a development dependency

```bash
# Install directly from GitHub
pip install git+https://github.com/your-org/shared-library.git@v1.0.0
```

Or add to your requirements.txt:

```
ai-shared-lib @ git+https://github.com/your-org/shared-library.git@v1.0.0
```

### For development

```bash
git clone https://github.com/your-org/shared-library.git
cd shared-library
pip install -e .
```

## Usage

```python
from ai_shared.auth import create_access_token
from ai_shared.prompts import get_system_prompt

# Create a JWT token
token = create_access_token({"sub": "user@example.com"})

# Get a system prompt for an agent
prompt = get_system_prompt("money")
```

## Development

See the CONTRIBUTING.md file for development guidelines.

## License

[MIT License](LICENSE)
