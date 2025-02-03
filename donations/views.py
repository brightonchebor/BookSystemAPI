from django.shortcuts import render
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book,MonetaryDonation,DonationCampaign
from .serializers import BookSerializer,MonetaryDonationSerializer,DonationCampaignSerializer


class BookDonationCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

class BookDonationListView(generics.ListAPIView):
    queryset = Book.objects.filter(availability_status='available')
    serializer_class= BookSerializer

class BookDonationDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly]

class BookDonationDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.donor == self.request.user:
            instance.delete()  

class MonetaryDonationCreateView(generics.CreateAPIView):
    queryset = MonetaryDonation.objects.all()
    serializer_class = MonetaryDonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

class DonationCampaignCreateView(generics.CreateAPIView):
    queryset = DonationCampaign.objects.all()
    serializer_class = DonationCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def perform_create(self, serializer):
        serializer.save()

class DonationCampaignListView(generics.ListAPIView):
    queryset = DonationCampaign.objects.all()
    serializer_class = DonationCampaignSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'start_date', 'end_date']

    