import requests
import json
from datetime import datetime
import base64
from django.conf import settings

def get_access_token():
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(auth_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    return response.json().get('access_token')

def generate_password():
    timespan = datetime.now().strftime('%Y%m%d%H%M%S%')
    password = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timespan}"
    return base64.b64encode(password.encode()).decode()

def initiate_stk_push(phone_number, amount):
    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": generate_password(),
        "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S%'),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 'amount',
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_nmber,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountRefrence": "BookDonation",
        "TransactionDesc": "Payment for book donation",
    }
    reponse = requests.post(api_url, headers=headers, data=json.dumps(payload))
    return reponse.json()