# 🚀 AfriRemotely Backend API

A Django REST Framework backend for connecting African talent with global remote job opportunities.

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#%EF%B8%8F-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Environment Variables](#-environment-variables)
- [Running the Server](#-running-the-server)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 👥 User Management
- **Three User Roles**: Job Seeker, Recruiter, and Admin
- **JWT Authentication**: Secure token-based authentication
- **Profile Management**: Update bio, skills, portfolio, and profile image
- **Recruiter Verification**: Admin verification system for recruiters

### 💼 Job Management
- **Job Posting**: Recruiters can create and manage job listings
- **Job Search**: Advanced filtering by location, type, category, and skills
- **Job Types**: Full-time, Part-time, Contract, Remote, Hybrid, Onsite
- **Active/Inactive Jobs**: Toggle job visibility

### 📄 Application System
- **Job Applications**: Job seekers can apply to jobs
- **Application Tracking**: Status updates (Submitted, Viewed, Shortlisted, Rejected, Hired)
- **Cover Letters**: Custom cover letters for each application
- **Resume Management**: URL-based resume storage

### 🛠️ Admin Features
- **User Management**: View, verify, and manage all users
- **Job Management**: Create, update, and delete any job
- **Application Oversight**: Monitor all applications
- **Recruiter Verification**: Approve recruiter accounts

### 🔍 Advanced Features
- **Skills Matching**: Basic job matching based on skills
- **Pagination**: Efficient data loading
- **Search & Filtering**: Comprehensive search functionality
- **API Documentation**: Interactive Swagger/OpenAPI docs

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Backend programming language |
| **Django 4.0+** | Web framework |
| **Django REST Framework** | API development |
| **PostgreSQL / SQLite** | Database (production/development) |
| **JWT Authentication** | Secure user authentication |
| **Django Filter** | Advanced query filtering |
| **CORS Headers** | Cross-origin resource sharing |
| **drf-yasg** | Swagger/OpenAPI documentation |
| **Python Decouple** | Environment configuration |

## 📁 Project Structure
