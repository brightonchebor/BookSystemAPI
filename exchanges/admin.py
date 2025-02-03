from django.contrib import admin


from .models import Book,ExchangeRequest

admin.site.register(Book)
admin.site.register(ExchangeRequest)
