from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'email', 'password', 'role',
            'bio', 'skills', 'portfolio_links', 'image_url',
            'is_verified', 'created_at'
        ]
        read_only_fields = ['created_at', 'is_verified']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            role=validated_data.get('role', 'job_seeker')
        )
        return user