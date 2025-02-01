from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_joined', 'last_login', 'role']
    
admin.site.register(Profile)
admin.site.register(OneTimePassword)
