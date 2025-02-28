"""
Shared Pydantic schemas for AI Projects.

This module provides Pydantic models used for API request/response validation
in both Money Machine and Safety Machine applications.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common attributes."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation requests."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for user update requests."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOut(UserBase):
    """Schema for user responses."""
    id: int
    credits: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class LoginInput(BaseModel):
    """Schema for login requests."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication tokens."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data."""
    email: Optional[str] = None


class TransactionBase(BaseModel):
    """Base transaction schema."""
    amount: float
    credits: int
    description: str


class TransactionCreate(TransactionBase):
    """Schema for transaction creation."""
    user_id: int
    payment_id: Optional[str] = None


class TransactionOut(TransactionBase):
    """Schema for transaction responses."""
    id: int
    user_id: int
    payment_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True


class AIQuery(BaseModel):
    """Schema for AI query requests."""
    prompt: str
    agent_type: Literal["money", "safety"]


class AIResponse(BaseModel):
    """Schema for AI query responses."""
    answer: str
    tokens_used: Optional[int] = None


class AIDecisionOut(BaseModel):
    """Schema for AI decision history responses."""
    id: int
    agent_type: str
    prompt: str
    response: str
    created_at: datetime
    
    class Config:
        orm_mode = True


class PaymentCreate(BaseModel):
    """Schema for payment creation requests."""
    amount: int = Field(..., gt=0)  # Amount in cents


class PaymentResponse(BaseModel):
    """Schema for payment creation responses."""
    checkout_url: str
