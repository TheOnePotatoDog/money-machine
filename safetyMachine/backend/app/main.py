"""
Main application module for Safety Machine.

This module initializes the FastAPI application, includes routers,
and configures middleware.
"""

import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import from shared library
from ai_shared.auth import create_access_token
from ai_shared.prompts import get_system_prompt
from ai_shared.models import Base

# Local imports
from .database import engine, get_db
from .routers import auth, users, ai, payments

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Safety Machine API",
    description="API for the Safety Machine AI risk assessment advisor",
    version="0.1.0"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])

@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "Safety Machine API"}
