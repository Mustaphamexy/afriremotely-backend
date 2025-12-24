# matching/urls.py
from django.urls import path
from .views import jobs_for_me, skill_analysis

urlpatterns = [
    path('jobs-for-me/', jobs_for_me, name='jobs-for-me'),
    path('skill-analysis/', skill_analysis, name='skill-analysis'),
]