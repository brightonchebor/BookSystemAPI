from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book, ExchangeRequest
from .serializers import BookSerializer,ExchangeRequestSerializer
from django_filter.rest_framework import DjangoFilterBackened
from rest_framework.filters import SearchFilter
from geopy.distance import geodesic
from rest_framework.response import Response
from rest_framework.views import APIView


class BookListCreateView(generics.ListCreateAPIView):
    queryset =Book.objects.filter(is_available=True)
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackened, SearchFilter]
    filterset_fields = ['subject', 'grade_level', 'location']
    search_fields = ['title', 'author', 'subject', 'grade_level', 'location']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ExchangeRequestCreateView(generics.CreateAPIView):
    queryset = ExchangeRequest.objects.all()
    serializer_class = ExchangeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs.get('id')
        book = Book.objects.get(id=book_id)
        serializer.save(requester=self.request.user, book=book)

class NearbyBooksView(APIView):
    def get(self, request):
        user_latitude = float(request.query_params.get('lat'))
        user_longitude = float(request.query_params.get('lon'))
        radius = float(request.query_params.get('radius', 10))

        nearby_books = [ ]
        for book in Book.objects.all():
            book_coords = (book.latitude, book.longitude)
            user_coords = (user_latitude, user_longitude)
            distance = geodesic(user_coords, book_coords).km

            if distance <= radius:
                nearby_books.append(book)
        
        serializer = BookSerializer(nearby_books, many=True)
        return Response(serializer.data)
