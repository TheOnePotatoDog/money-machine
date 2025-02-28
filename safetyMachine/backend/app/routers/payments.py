"""
Payments router for Safety Machine.

This module provides endpoints for payment processing.
"""

import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

# Import from shared library
from ai_shared.models import User, Transaction
from ai_shared.schemas import PaymentCreate, PaymentResponse
from ai_shared.clients import StripeClient

# Local imports
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter()
stripe_client = StripeClient()

@router.post("/create-checkout", response_model=PaymentResponse)
async def create_checkout_session(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a Stripe checkout session for purchasing credits.
    
    Args:
        payment: Payment creation data
        db: Database session
        current_user: The authenticated user
        
    Returns:
        PaymentResponse: Checkout URL
    """
    # Get frontend URL from environment
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Create checkout session
    session = stripe_client.create_checkout_session(
        customer_email=current_user.email,
        success_url=f"{frontend_url}/payment/success",
        cancel_url=f"{frontend_url}/payment/cancel",
        quantity=payment.amount // 1000  # $10 = 100 credits
    )
    
    if "error" in session:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating checkout session: {session['error']}"
        )
    
    return {"checkout_url": session["checkout_url"]}

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events.
    
    Args:
        request: The HTTP request
        db: Database session
        
    Returns:
        Dict: Status message
    """
    # Get the signature from headers
    signature = request.headers.get("stripe-signature")
    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe signature"
        )
    
    # Get the request body
    payload = await request.body()
    
    # Verify webhook
    result = stripe_client.verify_webhook(payload, signature)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid webhook: {result['error']}"
        )
    
    event = result["event"]
    
    # Handle checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        # Get customer email
        customer_email = session.get("customer_email")
        if not customer_email:
            return {"status": "error", "message": "No customer email in session"}
        
        # Find user by email
        user = db.query(User).filter(User.email == customer_email).first()
        if not user:
            return {"status": "error", "message": "User not found"}
        
        # Calculate credits (100 credits per $10)
        amount_paid = session.get("amount_total", 0)
        credits_to_add = (amount_paid // 1000) * 100
        
        # Add credits to user
        user.credits += credits_to_add
        
        # Create transaction record
        transaction = Transaction(
            user_id=user.id,
            amount=amount_paid / 100,  # Convert cents to dollars
            credits=credits_to_add,
            description=f"Purchased {credits_to_add} credits",
            payment_id=session.get("id")
        )
        
        db.add(transaction)
        db.commit()
    
    return {"status": "success"}
