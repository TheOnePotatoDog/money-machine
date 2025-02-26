#!/bin/bash

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your actual credentials before proceeding."
    echo "Press Enter to continue after editing, or Ctrl+C to cancel."
    read
fi

# Build and start the containers
echo "Building and starting containers..."
docker-compose up --build
