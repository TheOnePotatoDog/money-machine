"""
Shared database models for AI Projects.

This module provides SQLAlchemy ORM models used by both 
Money Machine and Safety Machine applications.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication and profile information."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    credits = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    ai_decisions = relationship("AIDecision", back_populates="user")


class Transaction(Base):
    """Transaction model for tracking credit purchases and usage."""
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)  # Positive for purchases, negative for usage
    credits = Column(Integer)  # Number of credits added/used
    description = Column(String)
    payment_id = Column(String, nullable=True)  # External payment reference (e.g., Stripe)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")


class AIDecision(Base):
    """AI Decision model for tracking AI queries and responses."""
    
    __tablename__ = "ai_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_type = Column(String)  # "money" or "safety"
    prompt = Column(Text)
    response = Column(Text)
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="ai_decisions")
