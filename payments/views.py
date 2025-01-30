from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .services.mpesa import initiate_stk_push
from .services.paypal import create_payment
from .services.stripe import create_payment_intent


class MpesaPaymentView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        amoount = request.data.get('amoount')
        response = initiate_stk_push(phone_number, amoount)
        return Response(response)
    
class PaypalPaymentView(APIView):
    def post(self, request):
        amount = request.data.get('amoount')
        redirect_url = create_payment(amount)
        if redirect_url:
            return Response({"redirect_url": redirect_url})
        else:
            return Response({"error": "payment creation failed"}, status=400)

class SrtipePaymentView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        client_secret = create_payment_intent(amount)
        if client_secret:
            return Response({"client_secret": client_secret})
        else:
            return Response({"error": "payment creation failed"}, status=400)