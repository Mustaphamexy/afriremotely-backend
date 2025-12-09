from rest_framework import serializers
from .models import Job
from users.serializers import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category',
            'required_skills', 'salary_range', 'location',
            'job_type', 'created_by', 'created_by_id',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']