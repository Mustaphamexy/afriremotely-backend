from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'job_seeker':
            return Application.objects.filter(job_seeker=user)
        elif user.role in ['recruiter', 'admin']:
            return Application.objects.filter(job__created_by=user)

        return Application.objects.none()

    def perform_create(self, serializer):
        job_id = self.request.data.get('job_id')
        job = get_object_or_404(Job, id=job_id, is_active=True)

        if Application.objects.filter(
            job_seeker=self.request.user,
            job=job
        ).exists():
            raise serializers.ValidationError(
                "You have already applied for this job"
            )

        serializer.save(
            job_seeker=self.request.user,
            job=job
        )

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Application.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if (
            request.user != application.job.created_by
            and request.user.role != 'admin'
        ):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        application.status = new_status
        application.save()

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """GET /applications/my/"""
        if request.user.role != 'job_seeker':
            return Response(
                {'error': 'Only job seekers can view their applications'},
                status=status.HTTP_403_FORBIDDEN
            )

        applications = self.get_queryset()
        page = self.paginate_queryset(applications)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def job_applications_detail(self, request, job_id=None):
        """GET /jobs/{job_id}/applications/"""

        if not job_id:
            job_id = request.query_params.get('job_id')

        if not job_id:
            return Response(
                {'error': 'job_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        job = get_object_or_404(Job, id=job_id)

        if (
            request.user != job.created_by
            and request.user.role != 'admin'
        ):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        applications = Application.objects.filter(job=job)
        serializer = self.get_serializer(applications, many=True)

        return Response({
            'job_title': job.title,
            'total_applications': applications.count(),
            'applications': serializer.data
        })

    @action(detail=True, methods=['post'], url_path='apply')
    def apply_for_job(self, request, pk=None):
        """POST /applications/{job_id}/apply/"""

        if request.user.role != 'job_seeker':
            return Response(
                {'error': 'Only job seekers can apply for jobs'},
                status=status.HTTP_403_FORBIDDEN
            )

        job = get_object_or_404(Job, id=pk, is_active=True)

        if Application.objects.filter(
            job_seeker=request.user,
            job=job
        ).exists():
            return Response(
                {'error': 'You have already applied for this job'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application = Application.objects.create(
            job_seeker=request.user,
            job=job,
            cover_letter=request.data.get('cover_letter', ''),
            resume_url=request.data.get('resume_url', '')
        )

        serializer = ApplicationSerializer(application)

        return Response(
            {
                'message': 'Application submitted successfully',
                'application': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
