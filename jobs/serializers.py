# jobs/serializers.py
from rest_framework import serializers
from .models import Job


class SimpleUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    image_url = serializers.URLField(read_only=True)

class JobSerializer(serializers.ModelSerializer):
    created_by = SimpleUserSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category',
            'required_skills', 'salary_range', 'location',
            'job_type', 'created_by', 'created_by_id',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        # Remove created_by_id if present
        validated_data.pop('created_by_id', None)
        return super().create(validated_data)