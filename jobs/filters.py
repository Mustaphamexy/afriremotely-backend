import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    min_salary = django_filters.CharFilter(field_name='salary_range', lookup_expr='gte')
    max_salary = django_filters.CharFilter(field_name='salary_range', lookup_expr='lte')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    job_type = django_filters.CharFilter(field_name='job_type')
    
    class Meta:
        model = Job
        fields = ['location', 'category', 'job_type', 'min_salary', 'max_salary']