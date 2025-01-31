from django.urls import path
from .views import BookListCreateView, BookDetailView, ExchangeRequestCreateView
from .views import NearbyBooksView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/exchange/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/exchange/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('api/exchange/request/<int:id>/', ExchangeRequestCreateView.as_view(), name='exchange-request'),
    path('api/exchange/books/nearby', NearbyBooksView.as_view(), name='nearby-books'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]