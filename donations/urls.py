from django.urls import path
from .views import (
    BookDonationCreateView, BookDonationListView, BookDonationDetailView, BookDonationDeleteView, MonetaryDonationCreateView, DonationCampaignListView
)


urlpatterns = [
    path('api/donations/books/', BookDonationCreateView.as_view(), name='book-donation-create'),
    path('api/donations/books/', BookDonationListView.as_view(), name='book-donation-list'),
    path('api/donations/books/<init:pk>/', BookDonationDetailView.as_view(), name='book-')
]