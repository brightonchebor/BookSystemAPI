from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
     condition_choices = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
     availability_coices =[
          ('available', 'Available'),
          ('donated', 'Donated'),
     ]
     title = models.CharField(max_length=200)
     author = models.CharField(max_length=100)
     condition = models.CharField(max_length=10, choices=condition_choices)
     subject_or_grade_level= models.CharField(max_length=10)
     image = models.ImageField(upload_to='book_images/', blank=True, null=True)
     availability_status = models.CharField(max_length=10, choices=availability_coices, default='available')
     donor = models.ForeignKey(User,on_delete=models.CASCADE, related_name='donated_books')
     timestamp = models.DateTimeField(default=timezone.now)

     def __str__(self):
          return self.title

class MonetaryDonation(models.Model):
     donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monetary_donations')
     amount = models.DecimalField(max_digits=10, decimal_places=2)
     payment_gateway = models.CharField(max_length=50, choices=[('mpesa', 'M-pesa'), ('paypal','Paypal'), ('stripe', 'Stripe')])
     timestamp = models.DateTimeField(default=timezone.now)

     def __str__(self):
         return f"{self.donor.username} - {self.amount}{self.payment_gateway}"


 
class DonationCampaign(models.Model):
     title = models.CharField(max_length=200)
     description = models.TextField()
     target_amount = models.DecimalField(max_digits=10, decimal_places=2)
     current_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
     start_date = models.DateTimeField(default=timezone.now)
     end_date = models.DateTimeField(null=True, blank=True)

     def save(self, *args, **kwargs):
          if not self.end_date:
               self.end_date = self.start_date + timedelta(days=30)
          super().save(*args, **kwargs)
     def __str__(self):
          return self.title
     


     
