# applications/models.py
from django.db import models

class Application(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("viewed", "Viewed"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    ]
    
    # Use string references instead of direct imports
    job_seeker = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="job_applications")
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    cover_letter = models.TextField(blank=True)
    resume_url = models.URLField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job_seeker', 'job']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.job_seeker.full_name} → {self.job.title} ({self.status})"