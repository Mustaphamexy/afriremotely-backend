# users/admin_views.py
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from jobs.models import Job


def get_job_serializer():
    from jobs.serializers import JobSerializer
    return JobSerializer

@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def verify_recruiter(request, id):
    try:
        recruiter = User.objects.get(id=id, role='recruiter')
    except User.DoesNotExist:
        return Response(
            {'error': 'Recruiter not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    recruiter.is_verified = True
    recruiter.save()
    
    from .serializers import UserListSerializer  # Import here
    return Response({
        'message': f'Recruiter {recruiter.email} has been verified',
        'recruiter': UserListSerializer(recruiter).data
    })

@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Prevent admin from deleting themselves
    if user == request.user:
        return Response(
            {'error': 'Cannot delete your own account'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    email = user.email
    user.delete()
    
    return Response({
        'message': f'User {email} has been deleted'
    })

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def admin_create_job(request):
    JobSerializer = get_job_serializer()  # Get serializer locally
    serializer = JobSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Admin can create jobs on behalf of any user
        created_by_id = request.data.get('created_by_id', request.user.id)
        try:
            created_by = User.objects.get(id=created_by_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job = serializer.save(created_by=created_by)
        return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def admin_delete_job(request, id):
    try:
        job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        return Response(
            {'error': 'Job not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    job.delete()
    return Response({
        'message': f'Job "{job.title}" has been deleted'
    })