# applications/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),

    # Custom ViewSet actions
    path(
        'applications/my/',
        ApplicationViewSet.as_view({'get': 'my_applications'}),
        name='my-applications'
    ),
    path(
        'jobs/<int:job_id>/applications/',
        ApplicationViewSet.as_view({'get': 'job_applications_detail'}),
        name='job-applications'
    ),
]
