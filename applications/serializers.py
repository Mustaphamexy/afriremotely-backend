from rest_framework import serializers
from .models import Application
from jobs.serializers import JobSerializer
from users.serializers import UserSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    job_seeker = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job_seeker', 'job', 'job_id',
            'status', 'cover_letter', 'resume_url',
            'applied_at', 'updated_at'
        ]
        read_only_fields = ['job_seeker', 'applied_at', 'updated_at']