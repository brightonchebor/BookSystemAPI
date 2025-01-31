from django.urls import path
from .views import BookListCreateView, BookDetailView, ExchangeRequestCreateView
from .views import NearbyBooksView


urlpatterns = [
    path('api/exchange/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/exchange/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('api/exchange/request/<int:id>/', ExchangeRequestCreateView.as_view(), name='exchange-request'),
    path('api/exchange/books/nearby', NearbyBooksView.as_view(), name='nearby-books'),
]