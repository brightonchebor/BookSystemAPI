from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book,MonetaryDonation,DonationCampaign
from .serializers import BookSerializer,MonetaryDonationSerializer,DonationCampaignSerializer

class BookDonationCreateView(generics.CreateApiView):
    queryset = Book.objects.all()
    BookSerializer_class = BookSerializer
    permission_class = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

class BookDonationListView(generics.ListAPIView):
    queryset = Book.objects.filter(availability_status='available')
    serializer_class = BookSerializer

class BookDonationDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDonationDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class DonationCampaignListView(generics.ListAPIView):
    queryset = DonationCampaign.objects.all()
    serializer_class = DonationCampaignSerializer