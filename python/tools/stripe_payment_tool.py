import stripe
from python.helpers.tool import Tool, Response
from python.helpers import files

class StripePayment(Tool):
    def execute(self, **kwargs):
        try:
            stripe.api_key = kwargs.get("api_key")
            
            payment_intent = stripe.PaymentIntent.create(
                amount=kwargs.get("amount"),
                currency=kwargs.get("currency"),
                description=kwargs.get("description"),
                customer=kwargs.get("customer_id", None),
                payment_method=kwargs.get("payment_method", None)
            )
            
            return Response(
                message=f"Payment intent created: {payment_intent.id}",
                break_loop=False
            )
        except Exception as e:
            return Response(
                message=f"Payment processing error: {str(e)}",
                break_loop=False
            ) 