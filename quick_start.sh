#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # For Unix/MacOS
# OR
# .\venv\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

echo "Please edit .env file with your Stripe API keys"
echo "Setup complete! You can now run the application" 