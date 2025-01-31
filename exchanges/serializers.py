from rest_framework import serializers
from .models import Book, ExchangeRequest

class BookSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')

    class Meta:
        model = Book
        fields = '__all__'

class ExchangeRequestSerializer(serializers.ModelSerializer):
    requester =serializers.ReadOnlyField(source='requester.username')

    class Meta:
        model = ExchangeRequest
        fields = '__all__'
        