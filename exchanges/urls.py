from django.urls import path
from .views import BookListCreateView, BookDetailView, ExchangeRequestCreateView,NearbyBooksView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/exchanges/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/exchanges/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('request/<int:id>/', ExchangeRequestCreateView.as_view(), name='exchange-request'),
    path('api/exchanges/books/nearby', NearbyBooksView.as_view(), name='nearby-books'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]