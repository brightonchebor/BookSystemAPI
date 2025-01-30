from django.urls import path
from .views import (
    BookDonationCreateView, BookDonationListView, BookDonationDetailView, BookDonationDeleteView, MonetaryDonationCreateView, DonationCampaignListView
)


urlpatterns = [
    path('api/donations/books/', BookDonationCreateView.as_view(), name='book-donation-create'),
    path('api/donations/books/', BookDonationListView.as_view(), name='book-donation-list'),
    path('api/donations/books/<int:pk>/', BookDonationDetailView.as_view(), name='book-donation-detail'),
    path('api/donations/books/<int:pk>/delete/', BookDonationDeleteView.as_view(),name='book-donation-delete'),
    path('api/donations/money/', MonetaryDonationCreateView.as_view(), name='monetary-donation-create'),
    path('api/donations/campaigns/', DonationCampaignListView.as_view(), name='donation-campaign-list'),
]