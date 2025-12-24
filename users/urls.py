# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    RegisterView, 
    LoginView, 
    UserProfileView,
    get_current_user
)
from . import admin_views  # Fixed import

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Profile
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('me/update/', UserProfileView.as_view(), name='update-profile'),
    path('current/', get_current_user, name='current-user'),
    
    # User lists
    path('job-seekers/', UserViewSet.as_view({'get': 'job_seekers'}), name='job-seekers'),
    path('recruiters/', UserViewSet.as_view({'get': 'recruiters'}), name='recruiters'),
    
    # Admin endpoints (fixed imports)
    path('admin/verify-recruiter/<int:id>/', 
         admin_views.verify_recruiter, 
         name='verify-recruiter'),
    path('admin/user/<int:id>/', 
         admin_views.delete_user, 
         name='delete-user'),
    path('admin/jobs/', 
         admin_views.admin_create_job, 
         name='admin-create-job'),
    path('admin/jobs/<int:id>/', 
         admin_views.admin_delete_job, 
         name='admin-delete-job'),
    
    # Include router URLs
    path('', include(router.urls)),
]