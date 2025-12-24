# AfriRemotely Backend API

**A Django REST Framework backend connecting African talent with global remote job opportunities**

---

## Overview

AfriRemotely is a comprehensive job platform API built with Django REST Framework, designed to bridge the gap between talented African professionals and international remote work opportunities. The platform features role-based access control, advanced job matching algorithms, and a complete application tracking system.

---

## Key Features

### User Management System
The platform supports three distinct user roles with customized permissions and capabilities:

**Job Seekers** can create profiles showcasing their skills, experience, and portfolio. They have access to job search functionality, can apply to multiple positions, and track their application status through an intuitive interface.

**Recruiters** can post job listings, manage their company's open positions, review applications, and update candidate statuses throughout the hiring process. All recruiter accounts undergo admin verification to ensure platform quality.

**Administrators** have complete system oversight, including user management, recruiter verification, job moderation, and platform analytics access.

### Job Management Capabilities
The job management system supports diverse employment types including full-time, part-time, contract, remote, hybrid, and onsite positions. Recruiters can create detailed job listings with skill requirements, salary ranges, and location specifications. Jobs can be toggled between active and inactive states, allowing recruiters to manage visibility without deleting listings.

Advanced search and filtering capabilities enable users to find opportunities by location, job type, category, required skills, and keywords. The search system is optimized for performance with pagination and efficient database queries.

### Application Tracking System
Job seekers can submit applications with custom cover letters and resume links. The system tracks application status through five stages: submitted, viewed, shortlisted, rejected, and hired. Recruiters receive organized views of all applicants for their job postings, while job seekers maintain a personal dashboard of all their applications.

### Intelligent Job Matching
The platform includes a skills-based matching algorithm that recommends relevant jobs to seekers based on their profile skills. The system also provides skill gap analysis, helping job seekers identify areas for professional development.

---

## Technology Stack

### Core Framework
**Django 4.2** serves as the foundational web framework, providing robust ORM capabilities, built-in security features, and excellent scalability. **Django REST Framework 3.14** extends Django with powerful API development tools, including serializers, viewsets, and authentication systems.

### Authentication & Security
**JWT (JSON Web Tokens)** via SimpleJWT provides stateless authentication with token refresh capabilities. **Django CORS Headers** enables secure cross-origin requests for frontend integration.

### Database & Querying
**PostgreSQL** is recommended for production environments, offering robust data integrity and advanced querying capabilities. **SQLite** serves as the default development database. **Django Filter** provides advanced query parameter filtering for complex search operations.

### API Documentation
**drf-yasg** generates interactive Swagger/OpenAPI documentation, enabling developers to explore and test API endpoints directly from the browser.

### Configuration Management
**Python Decouple** manages environment variables and configuration, separating sensitive data from code and enabling easy deployment across environments.

---

## Project Architecture

```
afriremotely/
│
├── users/                      # User management module
│   ├── models.py              # User model with role-based fields
│   ├── views.py               # User authentication & profile views
│   ├── admin_views.py         # Admin-specific user operations
│   ├── serializers.py         # User data serialization
│   └── urls.py                # User-related endpoints
│
├── jobs/                       # Job listings module
│   ├── models.py              # Job model with filtering fields
│   ├── views.py               # Job CRUD operations
│   ├── serializers.py         # Job data serialization
│   └── urls.py                # Job-related endpoints
│
├── applications/               # Application system module
│   ├── models.py              # Application model with status tracking
│   ├── views.py               # Application submission & management
│   ├── serializers.py         # Application data serialization
│   └── urls.py                # Application-related endpoints
│
├── matching/                   # Job matching algorithm
│   ├── views.py               # Matching logic & recommendations
│   └── urls.py                # Matching endpoints
│
├── afriremotely/              # Project settings
│   ├── settings.py            # Django configuration
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py                # WSGI application
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
└── README.md                   # Project documentation
```

---

## Installation Guide

### Prerequisites
Ensure you have Python 3.9 or higher installed on your system. You'll also need pip for package management and git for version control.

### Step-by-Step Setup

**Clone the repository** and navigate to the project directory:
```bash
git clone <repository-url>
cd afriremotely
```

**Create and activate a virtual environment** to isolate project dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Install all required dependencies** from the requirements file:
```bash
pip install -r requirements.txt
```

**Configure environment variables** by creating a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secure-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

**Initialize the database** by running migrations:
```bash
python manage.py migrate
```

**Create an administrative user** for platform management:
```bash
python manage.py createsuperuser
```

**Start the development server**:
```bash
python manage.py runserver
```

The API will be accessible at `http://localhost:8000`. Visit `http://localhost:8000/swagger/` for interactive API documentation.

---

## API Reference

### Authentication Endpoints

**User Registration** - `POST /api/users/register/`  
Creates a new user account with role selection (job_seeker, recruiter, or admin). Requires full_name, email, password, and role in the request body.

**User Login** - `POST /api/users/login/`  
Authenticates a user and returns JWT access and refresh tokens. Requires email and password.

**Token Generation** - `POST /api/token/`  
Obtains a new JWT token pair using user credentials.

**Token Refresh** - `POST /api/token/refresh/`  
Generates a new access token using a valid refresh token, extending the session without re-authentication.

### User Profile Endpoints

**Get Current User** - `GET /api/users/me/`  
Retrieves the authenticated user's complete profile including role-specific fields.

**Update Profile** - `PUT /api/users/me/update/`  
Updates user profile information including bio, skills, portfolio links, and profile image URL.

**List Job Seekers** - `GET /api/users/job-seekers/`  
Returns a paginated list of all job seeker profiles. Accessible to recruiters and administrators.

**List Recruiters** - `GET /api/users/recruiters/`  
Returns a paginated list of all recruiter profiles. Admin-only endpoint for user management.

### Administrative Endpoints

**Verify Recruiter** - `PUT /api/users/admin/verify-recruiter/{id}/`  
Approves a recruiter account, enabling them to post jobs. Requires admin authentication.

**Delete User** - `DELETE /api/users/admin/user/{id}/`  
Permanently removes a user account and all associated data. Admin-only operation.

**Admin Create Job** - `POST /api/users/admin/jobs/`  
Allows administrators to create job listings on behalf of any recruiter.

**Admin Delete Job** - `DELETE /api/users/admin/jobs/{id}/`  
Enables administrators to remove any job listing regardless of ownership.

### Job Management Endpoints

**List All Jobs** - `GET /api/jobs/jobs/`  
Returns all active job listings with pagination. Supports query parameters for filtering.

**Create Job** - `POST /api/jobs/jobs/`  
Creates a new job listing. Requires recruiter or admin authentication. Request body must include title, description, category, required_skills, salary_range, location, and job_type.

**Get Job Details** - `GET /api/jobs/jobs/{id}/`  
Retrieves complete information for a specific job listing including recruiter details.

**Update Job** - `PUT /api/jobs/jobs/{id}/`  
Modifies an existing job listing. Only the job creator or administrators can update jobs.

**Delete Job** - `DELETE /api/jobs/jobs/{id}/`  
Permanently removes a job listing. Restricted to job creator or administrators.

**Toggle Job Status** - `PATCH /api/jobs/jobs/{id}/toggle_active/`  
Switches a job between active and inactive states without deleting it.

**My Posted Jobs** - `GET /api/jobs/jobs/my_jobs/`  
Returns all jobs created by the authenticated recruiter.

### Job Search Endpoints

**Advanced Search** - `GET /api/jobs/jobs/search/`  
Performs multi-criteria search using query parameters: `location`, `job_type`, `category`, and `keyword`.

**Search by Location** - `GET /api/jobs/jobs/location/{location}/`  
Filters jobs by geographic location.

**Search by Job Type** - `GET /api/jobs/jobs/type/{job_type}/`  
Filters jobs by employment type (full-time, part-time, contract, remote, hybrid, onsite).

**Search by Skills** - `GET /api/jobs/jobs/skills/{skill}/`  
Finds jobs requiring specific technical skills.

**Search by Category** - `GET /api/jobs/jobs/category/{category}/`  
Filters jobs by industry or role category.

### Application Endpoints

**Apply for Job** - `POST /api/applications/applications/{job_id}/apply/`  
Submits a job application with cover letter and resume URL. Job seeker authentication required.

**My Applications** - `GET /api/applications/applications/my/`  
Retrieves all applications submitted by the authenticated job seeker with current status.

**View Job Applicants** - `GET /api/applications/jobs/{job_id}/applications/`  
Returns all applications for a specific job listing. Accessible to the job creator and administrators.

**Update Application Status** - `PATCH /api/applications/applications/{id}/update_status/`  
Changes application status (submitted, viewed, shortlisted, rejected, hired). Recruiter or admin only.

**List Applications** - `GET /api/applications/applications/`  
Returns applications based on user role: all applications for admins, job applications for recruiters, personal applications for job seekers.

**Create Application** - `POST /api/applications/applications/`  
Alternative endpoint for submitting job applications with full application details.

### Matching System Endpoints

**Job Recommendations** - `GET /api/match/jobs-for-me/`  
Analyzes the authenticated job seeker's skills and returns matching job recommendations ranked by relevance.

**Skill Gap Analysis** - `GET /api/match/skill-analysis/`  
Compares job seeker skills against available positions and identifies areas for professional development.

### System Health

**Health Check** - `GET /api/health/`  
Returns API status and basic system information for monitoring purposes.

---

## Database Schema

### User Model
The User model extends Django's AbstractUser with custom fields supporting the platform's role-based architecture.

**Core Fields:**
- `id` (Primary Key) - Auto-incrementing unique identifier
- `full_name` (String, required) - User's complete name
- `email` (String, unique, required) - Authentication email and username
- `password` (String, hashed) - Securely stored password hash
- `role` (Choice Field) - User type: job_seeker, recruiter, or admin

**Profile Fields:**
- `bio` (Text, optional) - Brief professional summary
- `skills` (JSON, optional) - Array of technical and soft skills for job seekers
- `portfolio_links` (JSON, optional) - Array of URLs to projects or profiles
- `image_url` (String, optional) - Profile picture URL

**Verification Fields:**
- `is_verified` (Boolean) - Admin approval status for recruiters
- `created_at` (DateTime) - Account creation timestamp
- `updated_at` (DateTime) - Last profile update timestamp

### Job Model
The Job model represents employment opportunities with comprehensive filtering capabilities.

**Identification:**
- `id` (Primary Key) - Unique job identifier
- `created_by` (Foreign Key → User) - Reference to recruiter or admin who posted the job

**Job Details:**
- `title` (String, required) - Position title
- `description` (Text, required) - Detailed job description and responsibilities
- `category` (String, required) - Industry or role category
- `required_skills` (JSON, required) - Array of necessary technical skills
- `salary_range` (String, required) - Compensation information
- `location` (String, required) - City, country, or "Remote"
- `job_type` (Choice Field) - Employment type: full-time, part-time, contract, remote, hybrid, onsite

**Status Fields:**
- `is_active` (Boolean) - Whether job is visible in searches
- `created_at` (DateTime) - Job posting timestamp
- `updated_at` (DateTime) - Last modification timestamp

### Application Model
The Application model tracks the hiring process from submission to final decision.

**Relationships:**
- `id` (Primary Key) - Unique application identifier
- `job_seeker_id` (Foreign Key → User) - Applicant reference
- `job_id` (Foreign Key → Job) - Job being applied for

**Application Content:**
- `cover_letter` (Text, required) - Customized application message
- `resume_url` (URL, required) - Link to applicant's resume

**Status Tracking:**
- `status` (Choice Field) - Current stage: submitted, viewed, shortlisted, rejected, hired
- `applied_at` (DateTime) - Initial submission timestamp
- `updated_at` (DateTime) - Last status change timestamp

### Data Relationships

**User to Job Relationship (One-to-Many)**  
A single recruiter or administrator can create multiple job listings. This relationship enables recruiters to manage their company's hiring pipeline and track all positions they've posted.

**User to Application Relationship (One-to-Many)**  
A job seeker can submit multiple applications to different positions. This allows candidates to pursue several opportunities simultaneously while maintaining organized application tracking.

**Job to Application Relationship (One-to-Many)**  
Each job listing can receive multiple applications from different candidates. This structure enables recruiters to compare candidates and manage the hiring process efficiently.

---

## Configuration & Deployment

### Environment Variables
Create a `.env` file in the project root with the following variables:

```env
# Debug mode (set to False in production)
DEBUG=True

# Django secret key (generate a new one for production)
SECRET_KEY=your-secure-random-secret-key

# Database configuration
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost:5432/afriremotely

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# CORS configuration
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourfrontend.com

# JWT token lifetime (in minutes)
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080
```

### Production Deployment

**Heroku Deployment:**
```bash
# Install Heroku CLI and login
heroku login

# Create a new Heroku app
heroku create afriremotely-api

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret-key

# Deploy the application
git push heroku main

# Run database migrations
heroku run python manage.py migrate

# Create admin user
heroku run python manage.py createsuperuser

# Open the application
heroku open
```

**Docker Deployment:**
Create a `Dockerfile` in the project root:
```dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
```

Create a `docker-compose.yml` for local development:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: afriremotely
      POSTGRES_USER: afriuser
      POSTGRES_PASSWORD: afripass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://afriuser:afripass@db:5432/afriremotely
    depends_on:
      - db

volumes:
  postgres_data:
```

---

## Testing

### Running Tests
Execute the complete test suite:
```bash
python manage.py test
```

Run tests for specific modules:
```bash
python manage.py test users
python manage.py test jobs
python manage.py test applications
python manage.py test matching
```

### Test Coverage
Generate a coverage report:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Writing Tests
Create test files following Django's conventions:
```python
from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            role='job_seeker'
        )
    
    def test_user_registration(self):
        response = self.client.post('/api/users/register/', {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'full_name': 'New User',
            'role': 'job_seeker'
        })
        self.assertEqual(response.status_code, 201)
```

---

## Quick Fixes & Improvements

### Fix URL Configuration
Update `users/urls.py` to properly import admin views:

```python
from django.urls import path
from . import views, admin_views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('me/', views.get_current_user, name='current-user'),
    path('me/update/', views.update_profile, name='update-profile'),
    
    # User listing endpoints
    path('job-seekers/', views.list_job_seekers, name='list-job-seekers'),
    path('recruiters/', views.list_recruiters, name='list-recruiters'),
    
    # Admin endpoints
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
]
```

### Complete Requirements File
Ensure your `requirements.txt` includes all necessary dependencies:

```text
Django==4.2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.2.0
django-filter==23.3
django-extensions==3.2.3
drf-yasg==1.21.7
python-decouple==3.8
psycopg2-binary==2.9.7
pillow==10.1.0
```

---

## Contributing

We welcome contributions from the community! Follow these steps to contribute:

**Fork the Repository** - Create your own copy of the project on GitHub.

**Create a Feature Branch** - Branch off from main with a descriptive name:
```bash
git checkout -b feature/job-bookmarking
```

**Make Your Changes** - Implement your feature or fix, following Django and Python best practices.

**Write Tests** - Ensure your changes include appropriate test coverage.

**Commit Your Changes** - Use clear, descriptive commit messages:
```bash
git commit -m "Add job bookmarking functionality for job seekers"
```

**Push to Your Fork** - Upload your branch to GitHub:
```bash
git push origin feature/job-bookmarking
```

**Open a Pull Request** - Submit your changes for review with a detailed description.

### Code Standards
- Follow PEP 8 style guidelines for Python code
- Write docstrings for all functions and classes
- Maintain test coverage above 80%
- Use meaningful variable and function names
- Keep functions focused and concise

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software with attribution.

---

## Support & Contact

For questions, bug reports, or feature requests:
- Open an issue on GitHub
- Contact the development team at support@afriremotely.com
- Join our community Slack channel

---

**AfriRemotely** - Empowering African talent to access global remote opportunities since 2024.

*Built with ❤️ by developers who believe in the power of remote work to transform careers and communities across Africa.*