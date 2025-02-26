# Project Setup and Local Development Guide

This guide will help you set up and run the project locally using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Git

## Setup Steps

### 1. Clone the repository

```bash
git clone <repository-url>
cd project-root
```

### 2. Set up environment variables

Create a `.env` file by copying the example file:

```bash
cp .env.example .env
```

Then edit the `.env` file to add your actual credentials:
- Generate a strong random string for `SECRET_KEY`
- Add your Stripe API keys from the Stripe dashboard
- Add your OpenAI API key if you're using OpenAI

### 3. Build and start the containers

```bash
docker-compose up --build
```

This command will:
- Build the Docker images for frontend and backend
- Start the PostgreSQL database
- Start the backend service on port 8000
- Start the frontend service on port 3000

### 4. Access the application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Viewing logs

```bash
docker-compose logs -f
```

To view logs for a specific service:

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Stopping the application

```bash
docker-compose down
```

To remove volumes (this will delete the database data):

```bash
docker-compose down -v
```

### Rebuilding after changes

If you make changes to the code, you'll need to rebuild the containers:

```bash
docker-compose up --build
```

## Troubleshooting

### Database connection issues

If the backend can't connect to the database, ensure:
1. The database container is running: `docker-compose ps`
2. The `DATABASE_URL` in your `.env` file matches the configuration in `docker-compose.yaml`

### API connection issues from frontend

If the frontend can't connect to the backend API, check:
1. Both services are running: `docker-compose ps`
2. The API URL in the frontend configuration is correct

## Data Persistence

Database data is stored in a Docker volume named `db-data`. This ensures your data persists between container restarts.
