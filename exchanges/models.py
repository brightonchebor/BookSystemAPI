from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100) 
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='uploaded_books')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Request for {self.title} by {self.author}"


class ExchangeRequest(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    requester = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")])

    def __str__(self):
        return f"{self.requester} - {self.book.title}"