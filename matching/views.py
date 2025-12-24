# matching/views.py
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q

# Import locally to avoid circular imports
def get_job_serializer():
    from jobs.serializers import JobSerializer
    return JobSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def jobs_for_me(request):
    """GET /match/jobs-for-me - Suggest jobs based on skills"""
    from jobs.models import Job
    
    user = request.user
    
    if user.role != 'job_seeker':
        return Response(
            {'error': 'This endpoint is only for job seekers'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_skills = user.skills or []
    if not user_skills:
        return Response({
            'message': 'Add skills to your profile to get job matches',
            'suggested_jobs': []
        })
    
    # Get all active jobs
    jobs = Job.objects.filter(is_active=True)
    
    # Score jobs based on skill match
    scored_jobs = []
    for job in jobs:
        job_skills = job.required_skills or []
        
        # Calculate match score
        if job_skills:
            # Convert to sets for comparison
            user_skill_set = set(user_skills)
            job_skill_set = set(job_skills)
            
            # Calculate matching skills
            matching_skills = user_skill_set.intersection(job_skill_set)
            
            # Calculate match percentage
            if job_skill_set:
                match_percentage = (len(matching_skills) / len(job_skill_set)) * 100
            else:
                match_percentage = 0
            
            # Only include jobs with at least 30% match
            if match_percentage >= 30:
                scored_jobs.append({
                    'job': job,
                    'match_score': match_percentage,
                    'matching_skills': list(matching_skills),
                    'missing_skills': list(job_skill_set - user_skill_set)
                })
    
    # Sort by match score (highest first)
    scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Prepare response
    JobSerializer = get_job_serializer()
    result = []
    for scored_job in scored_jobs[:10]:  # Return top 10 matches
        job_data = JobSerializer(scored_job['job']).data
        job_data['match_score'] = round(scored_job['match_score'], 2)
        job_data['matching_skills'] = scored_job['matching_skills']
        job_data['missing_skills'] = scored_job['missing_skills']
        result.append(job_data)
    
    return Response({
        'user_skills': user_skills,
        'total_matches_found': len(scored_jobs),
        'suggested_jobs': result
    })
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def skill_analysis(request):
    """GET /match/skill-analysis - Analyze user's skills"""

    user = request.user

    if user.role != 'job_seeker':
        return Response(
            {'error': 'This endpoint is only for job seekers'},
            status=status.HTTP_403_FORBIDDEN
        )

    user_skills = user.skills or []

    if not user_skills:
        return Response({
            'message': 'No skills found. Add skills to your profile.',
            'skills_count': 0,
            'skills': []
        })

    return Response({
        'skills_count': len(user_skills),
        'skills': user_skills,
        'analysis': 'Skills successfully analyzed'
    })
