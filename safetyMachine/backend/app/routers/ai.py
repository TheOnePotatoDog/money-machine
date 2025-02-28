"""
AI router for Safety Machine.

This module provides endpoints for interacting with the Safety Machine AI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import from shared library
from ai_shared.schemas import AIQuery, AIResponse, AIDecisionOut
from ai_shared.models import User, AIDecision
from ai_shared.clients import OpenAIClient
from ai_shared.prompts import get_system_prompt

# Local imports
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter()
openai_client = OpenAIClient()

@router.post("/query", response_model=AIResponse)
async def query_ai(
    query: AIQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Query the Safety Machine AI.
    
    Args:
        query: The AI query containing prompt and agent type
        db: Database session
        current_user: The authenticated user
        
    Returns:
        AIResponse: The AI's response
    """
    # Check if user has enough credits
    if current_user.credits <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Not enough credits. Please purchase more credits to continue."
        )
    
    # Ensure agent type is "safety"
    if query.agent_type != "safety":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid agent type. Must be 'safety' for this endpoint."
        )
    
    # Get system prompt for safety agent
    system_prompt = get_system_prompt("safety")
    
    # Generate AI response
    response = openai_client.generate_completion(
        system_prompt=system_prompt,
        user_prompt=query.prompt,
        temperature=0.7,
        max_tokens=1000
    )
    
    if "error" in response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating AI response: {response['error']}"
        )
    
    # Deduct one credit from user
    current_user.credits -= 1
    db.commit()
    
    # Log the AI decision
    ai_decision = AIDecision(
        user_id=current_user.id,
        agent_type=query.agent_type,
        prompt=query.prompt,
        response=response["text"],
        tokens_used=response.get("tokens_used")
    )
    db.add(ai_decision)
    db.commit()
    
    return AIResponse(
        answer=response["text"],
        tokens_used=response.get("tokens_used")
    )

@router.get("/history", response_model=List[AIDecisionOut])
async def get_ai_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the user's AI query history.
    
    Args:
        db: Database session
        current_user: The authenticated user
        
    Returns:
        List[AIDecisionOut]: List of AI decisions
    """
    decisions = db.query(AIDecision).filter(
        AIDecision.user_id == current_user.id
    ).order_by(AIDecision.created_at.desc()).all()
    
    return decisions
