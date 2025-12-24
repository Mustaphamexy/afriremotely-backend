from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer
from .filters import JobFilter
from django.db.models import Q

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'category', 'location']
    ordering_fields = ['created_at', 'salary_range']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        job = self.get_object()
        job.is_active = not job.is_active
        job.save()
        return Response({'status': 'success', 'is_active': job.is_active})
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply custom filters
        location = request.query_params.get('location')
        job_type = request.query_params.get('job_type')
        category = request.query_params.get('category')
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_jobs(self, request):
        jobs = Job.objects.filter(created_by=request.user)
        page = self.paginate_queryset(jobs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def filter_by_location(self, request, location=None):
        """GET /jobs/location/{location}"""
        if not location:
            location = request.query_params.get('location', '')
        
        queryset = self.get_queryset().filter(location__icontains=location)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def filter_by_type(self, request, job_type=None):
        """GET /jobs/type/{job_type}"""
        if not job_type:
            job_type = request.query_params.get('type', '')
        
        if job_type not in dict(Job.JOB_TYPES):
            return Response(
                {'error': f'Invalid job type. Must be one of: {", ".join([t[0] for t in Job.JOB_TYPES])}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(job_type=job_type)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def filter_by_skills(self, request, skill=None):
        """GET /jobs/skills/{skill}"""
        if not skill:
            skill = request.query_params.get('skill', '')
        
        # Search in required_skills JSON field
        queryset = self.get_queryset().filter(
            Q(required_skills__contains=[skill]) | 
            Q(required_skills__icontains=skill)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def filter_by_category(self, request, category=None):
        """GET /jobs/category/{category}"""
        if not category:
            category = request.query_params.get('category', '')
        
        queryset = self.get_queryset().filter(category__icontains=category)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search_keyword(self, request):
        """GET /jobs/search?keyword=..."""
        keyword = request.query_params.get('keyword', '')
        
        if not keyword:
            return Response(
                {'error': 'Keyword parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(category__icontains=keyword) |
            Q(location__icontains=keyword)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)