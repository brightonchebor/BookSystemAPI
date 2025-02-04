from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:

        model = User
        fields = ['id','email', 'first_name', 'last_name', 'role', 'password', 'password2']

    def validate(self, attr):

        password = attr.get('password', '')
        password2 = attr.get('password2', '')
        if password != password2:
            raise serializers.ValidationError('passwords do not match')
        return attr

    def create(self, validated_data):
        
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            role = validated_data['role'],
            password = validated_data['password']
        )

        return user

class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=60, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [ 'email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        
        if not user:
            raise AuthenticationFailed("invalid credentials try again")

        if not user.is_verified:
            raise AuthenticationFailed("email is not verified")
         
        user_tokens = user.tokens() 

        return {
            'email':user.email,
            'full_name':user.get_full_name,
            'access_token':str(user_tokens.get('access')),
            'refresh_token':str(user_tokens.get('refresh')),

        }    
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email =serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email') 
        if User.objects.filter(email=email).exists(): # check if user is in the database
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('password-reset-confirm', kwargs={
                'uidb64':uidb64,
                'token':token
            })
            abslink = f'http://{site_domain}{relative_link}'
            email_body = f'Hi use the link below to reset your email \n {abslink}'
            data = {
                'email_body':email_body,
                'email_subject':'reset your password',
                'to_email':user.email
            }
            send_normal_email(data)
        return super().validate(attrs)        
    
class  SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('reset link is invalid or has expired', 401)
            if password != confirm_password:
                raise AuthenticationFailed('password does not match')
        
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed('link is invalid or has expired')
          
class LogoutUsererializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_message = {
        'key':('Token is invalid or has expired')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')

        return attrs
    def save(self, **kwarags):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')  
        

    
class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'profile_picture']

    def create(self, validated_data):
        user = self.context.get('user')
        profile = Profile.objects.create(user=user, **validated_data)
        
        # You can add logic for role-specific fields
        if user.role == 'donor':
            profile.donation_history = []
        elif user.role == 'recipient':
            profile.books_exchanged = []

        profile.save()
        return profile

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'profile_picture']

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        
        # Add logic to handle role-specific updates if necessary
        if instance.user.role == 'donor':
            instance.donation_history = validated_data.get('donation_history', instance.donation_history)
        elif instance.user.role == 'recipient':
            instance.books_exchanged = validated_data.get('books_exchanged', instance.books_exchanged)

        instance.save()
        return instance    