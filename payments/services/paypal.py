import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def create_payment(amount):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls":{
            "return_url": "https://yourdomain.com/payment/success/",
            "cancel_url": "https://yourdomain.com/payment/cancel/",
        },
        "transactions": [{
            "amount": {
                "total": amount,
                "currency": "USD",
            },
            "description": "payment for book donation",
        }],
        
    })
    
    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return link.href
    else:
        return None