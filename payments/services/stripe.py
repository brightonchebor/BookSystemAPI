import stripe
from django.conf import settings

stripe.api_key  = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount):
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),
            currency="usd",
            description="Payment for book donation",
        )
        return intent.client_secret
    except Exception as e:
        return None