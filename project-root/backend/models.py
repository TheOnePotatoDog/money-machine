from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    credits = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    decisions = relationship("AIDecision", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer)          # positive for credit, negative for usage
    type = Column(String(50))         # e.g. "purchase" or "usage"
    stripe_session_id = Column(String(255))
    timestamp = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="transactions")

class AIDecision(Base):
    __tablename__ = "ai_decisions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_type = Column(String(50))   # "money" or "safety"
    prompt = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="decisions")
