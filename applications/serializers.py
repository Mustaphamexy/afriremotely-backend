# applications/serializers.py
from rest_framework import serializers
from .models import Application

class SimpleUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    image_url = serializers.URLField(read_only=True)

class SimpleJobSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True, source='created_by.full_name')
    location = serializers.CharField(read_only=True)
    job_type = serializers.CharField(read_only=True)
    salary_range = serializers.CharField(read_only=True)

class ApplicationSerializer(serializers.ModelSerializer):
    job_seeker = SimpleUserSerializer(read_only=True)
    job = SimpleJobSerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job_seeker', 'job', 'job_id',
            'status', 'cover_letter', 'resume_url',
            'applied_at', 'updated_at'
        ]
        read_only_fields = ['job_seeker', 'applied_at', 'updated_at']