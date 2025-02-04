from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    
    path('api/auth/register/', UserRegisterView.as_view(), name='register'),
    path('api/auth/verify-email/', VerifyUserEmail.as_view(), name='verify'),
    path('api/auth/login/', LoginUserView.as_view(), name='login'),
    # path('profile/', TestAunthenticationView.as_view(), name='granted'),
    path('api/auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('api/auth/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('api/auth/set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('api/auth/logout/', LogoutUserView.as_view(), name='logout'),

    path('api/auth/profile/create/', ProfileCreateView.as_view(), name='profile-create'),
    path('api/auth/update/', ProfileUpdateView.as_view(), name='profile-update'),
]
