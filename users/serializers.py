# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password2', 'role', 'bio']
        extra_kwargs = {
            'role': {'default': 'job_seeker'},
            'bio': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Recruiters need admin approval
        if attrs.get('role') == 'recruiter':
            attrs['is_verified'] = False
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'bio', 'skills', 
                 'portfolio_links', 'image_url', 'is_verified', 'created_at']
        read_only_fields = ['id', 'email', 'role', 'is_verified', 'created_at']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'bio', 'skills', 'portfolio_links', 'image_url']
        
    def update(self, instance, validated_data):
        # Handle skills and portfolio_links updates
        if 'skills' in validated_data:
            instance.skills = validated_data['skills']
        if 'portfolio_links' in validated_data:
            instance.portfolio_links = validated_data['portfolio_links']
        
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()
        return instance

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'role', 'bio', 'skills', 'image_url', 'is_verified']