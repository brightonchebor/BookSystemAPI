from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Book, ExchangeRequest
from .serializers import BookSerializer, ExchangeRequestSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from geopy.distance import geodesic
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse


class BookListCreateView(generics.ListCreateAPIView):
    queryset =Book.objects.filter(is_available=True)
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['subject', 'grade_level', 'location']
    search_fields = ['title', 'author', 'subject', 'grade_level', 'location']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

class ExchangeRequestCreateView(generics.CreateAPIView):
    queryset = ExchangeRequest.objects.all()
    serializer_class = ExchangeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs.get('id')
        book = Book.objects.get(id=book_id)
        requester =self.request.user
        serializer.save(requester=self.request.user, book=book)
        subject = f"New Exchange Request for {book.title}"
        message = f"{requester.username} hass requested to exchange your book: {book.title}.\n\Message: {serializer.validated_data.get('message', '')}"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [book.uploaded_by.email],
            fail_silently=False,
        )
    #def get_exchange_request_model():
    #from .models import ExchangeRequest
    #return ExchangeRequest

class NearbyBooksView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request):
        try:
            user_latitude = float(request.query_params.get('lat'))
            user_longitude = float(request.query_params.get('lon'))
        except:
            return Response({"error": "Both 'lat' and 'lon' parameters are required and must be valid numbers."}, status=400)
        
        radius = float(request.query_params.get('radius', 10))
            
       

        nearby_books = [ ]
        for book in Book.objects.all():
            if book.latitude and book.longitude: 
                book_coords = (book.latitude, book.longitude)
                user_coords = (user_latitude, user_longitude)
                distance = geodesic(user_coords, book_coords).km

                if distance <= radius:
                    nearby_books.append(book)
        
        serializer = BookSerializer(nearby_books, many=True)
        return Response(serializer.data)
        
        #def get(self, request):
            #return JsonResponse({'message': 'NearbyBooksView is working'})