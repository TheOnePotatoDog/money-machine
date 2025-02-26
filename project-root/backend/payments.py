import os
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
from .auth import get_current_user
from .database import get_db
from . import models

# Stripe secret keys (from environment/Doppler)
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")  # Base URL of frontend

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter()

@router.post("/checkout")
def create_checkout_session(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Create a Stripe Checkout session for purchasing credits."""
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Credit Pack"},
                    "unit_amount": 1000  # $10.00 in cents (price for credits pack)
                },
                "quantity": 1
            }],
            mode="payment",
            client_reference_id=str(current_user.id),  # attach user ID for reference
            success_url=f"{FRONTEND_URL}/payment/success",
            cancel_url=f"{FRONTEND_URL}/payment/cancel"
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        # On failure, return error message
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Stripe webhook endpoint to handle payment events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe signature header")
    # Verify webhook signature
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="Webhook signature verification failed")
    # Handle successful checkout completion
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if session.get("payment_status") == "paid":
            user_id = session.get("client_reference_id")
            if user_id:
                user = db.query(models.User).filter(models.User.id == int(user_id)).first()
                if user:
                    # Credit the user's account (e.g., 100 credits for this purchase)
                    user.credits += 100
                    transaction = models.Transaction(
                        user_id=user.id, amount=100, type="purchase", 
                        stripe_session_id=session.get("id"), timestamp=datetime.utcnow()
                    )
                    db.add(transaction)
                    db.commit()
    return {"status": "success"}
