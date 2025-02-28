"""
API client wrappers for external services.

This module provides client classes for interacting with external APIs
like OpenAI, Stripe, etc., used by both Money Machine and Safety Machine.
"""

import os
import openai
from typing import Dict, Any, Optional, List


class OpenAIClient:
    """Client for interacting with OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        openai.api_key = self.api_key
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    
    def generate_completion(
        self, 
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Generate a completion using OpenAI's chat completion API.
        
        Args:
            system_prompt: The system prompt to guide the model
            user_prompt: The user's input prompt
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens in the response
            
        Returns:
            Dict containing the response and metadata
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "text": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason
            }
        except Exception as e:
            return {
                "error": str(e),
                "text": "I encountered an error while processing your request."
            }


class StripeClient:
    """Client for interacting with Stripe API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Stripe client.
        
        Args:
            api_key: Stripe API key (defaults to environment variable)
        """
        try:
            import stripe
            self.stripe = stripe
            self.api_key = api_key or os.getenv("STRIPE_SECRET_KEY")
            if not self.api_key:
                raise ValueError("Stripe API key is required")
            
            self.stripe.api_key = self.api_key
            self.price_id = os.getenv("STRIPE_PRICE_ID")
            self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        except ImportError:
            raise ImportError("Stripe package is not installed. Run 'pip install stripe'")
    
    def create_checkout_session(
        self, 
        customer_email: str,
        success_url: str,
        cancel_url: str,
        quantity: int = 1
    ) -> Dict[str, Any]:
        """
        Create a Stripe checkout session.
        
        Args:
            customer_email: Customer's email address
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect after cancelled payment
            quantity: Quantity of the product to purchase
            
        Returns:
            Dict containing the checkout session URL and ID
        """
        try:
            if not self.price_id:
                raise ValueError("Stripe price ID is required")
                
            session = self.stripe.checkout.Session.create(
                customer_email=customer_email,
                payment_method_types=["card"],
                line_items=[{
                    "price": self.price_id,
                    "quantity": quantity,
                }],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )
            
            return {
                "checkout_url": session.url,
                "session_id": session.id
            }
        except Exception as e:
            return {"error": str(e)}
    
    def verify_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """
        Verify a Stripe webhook signature.
        
        Args:
            payload: The raw request payload
            signature: The Stripe signature header
            
        Returns:
            Dict containing the verified event
        """
        try:
            if not self.webhook_secret:
                raise ValueError("Stripe webhook secret is required")
                
            event = self.stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            
            return {"event": event}
        except self.stripe.error.SignatureVerificationError:
            return {"error": "Invalid signature"}
        except Exception as e:
            return {"error": str(e)}
