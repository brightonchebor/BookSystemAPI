from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book,MonetaryDonation,DonationCampaign
from .serializers import BookSerializer, MonetaryDonationSerializer,


