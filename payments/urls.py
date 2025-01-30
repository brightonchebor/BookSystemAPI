from django.urls import path
from .views import MpesaPaymentView,PaypalPaymentView,SrtipePaymentView

urlpatterns = [
    path('mpesa/', MpesaPaymentView.as_view(), name='mpesa-payment'),
    path('paypal/', PaypalPaymentView.as_view(), name='paypal-payment'),
    path('stripe', SrtipePaymentView.as_view(), name='stripe-payment'),
]