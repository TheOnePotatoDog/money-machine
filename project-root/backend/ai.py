import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .auth import get_current_user
from .database import get_db
from . import models, schemas

# System prompts to guide the AI's behavior for each agent type
SYSTEM_PROMPT_MONEY = "You are Money Machine, an AI assistant specialized in financial decisions and advice."
SYSTEM_PROMPT_SAFETY = "You are Safety Machine, an AI assistant specialized in safety and risk assessment advice."

COST_PER_QUERY = 1  # cost in credits for each AI query

router = APIRouter()

@router.post("/query")
def ask_ai(query: schemas.AIQuery, 
           db: Session = Depends(get_db), 
           current_user: models.User = Depends(get_current_user)):
    """Handle an AI query from the user (Money or Safety agent). Deduct credits and return AI response."""
    # Ensure user has enough credits
    if current_user.credits < COST_PER_QUERY:
        raise HTTPException(status_code=400, detail="Not enough credits. Please purchase more to continue.")
    prompt = query.prompt
    agent_type = query.agent.lower()
    
    # Mock AI response since we don't have API keys
    if agent_type == "money":
        answer = f"[MONEY MACHINE MOCK RESPONSE] Here's financial advice about: {prompt}"
    else:
        answer = f"[SAFETY MACHINE MOCK RESPONSE] Here's safety advice about: {prompt}"

    # Deduct credits and log the interaction in the database
    current_user.credits -= COST_PER_QUERY
    decision = models.AIDecision(
        user_id=current_user.id, agent_type=agent_type, 
        prompt=prompt, response=answer, timestamp=datetime.utcnow()
    )
    transaction = models.Transaction(
        user_id=current_user.id, amount=-COST_PER_QUERY, type="usage", timestamp=datetime.utcnow()
    )
    db.add(decision)
    db.add(transaction)
    db.commit()
    db.refresh(current_user)  # refresh user to get updated credits
    return {"answer": answer}

@router.post("/free-credits")
def add_free_credits(db: Session = Depends(get_db), 
                    current_user: models.User = Depends(get_current_user)):
    """Add free credits for testing purposes"""
    current_user.credits += 10
    transaction = models.Transaction(
        user_id=current_user.id, amount=10, type="free", timestamp=datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(current_user)
    return {"message": "Added 10 free credits", "current_credits": current_user.credits}
