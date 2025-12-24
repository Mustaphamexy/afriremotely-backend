# jobs/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
    
    # Specific filter endpoints
    path('jobs/search/', JobViewSet.as_view({'get': 'search_keyword'}), name='job-search-keyword'),
    path('jobs/location/<str:location>/', JobViewSet.as_view({'get': 'filter_by_location'}), name='job-filter-location'),
    path('jobs/type/<str:job_type>/', JobViewSet.as_view({'get': 'filter_by_type'}), name='job-filter-type'),
    path('jobs/skills/<str:skill>/', JobViewSet.as_view({'get': 'filter_by_skills'}), name='job-filter-skills'),
    path('jobs/category/<str:category>/', JobViewSet.as_view({'get': 'filter_by_category'}), name='job-filter-category'),
]