# NextStep Careers User Documentation

## Overview
NextStep Careers is a Django-based job platform built for job seekers and employers. It supports user registration, profile management, job posting, search and filtering, applications, messaging, and notifications.

## Getting Started
1. Activate the workspace virtual environment.
   - PowerShell: `.\myworld\Scripts\Activate.ps1`
   - CMD: `myworld\Scripts\activate.bat`
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Run database migrations:
   ```powershell
   python manage.py migrate
   ```
4. Start the development server:
   ```powershell
   python manage.py runserver
   ```
5. Open `http://127.0.0.1:8000/` in your browser.

## User Roles
- **Job seeker**: Create a detailed profile, search jobs, apply to jobs, and message employers.
- **Employer**: Post job listings, manage job postings, review applications, and communicate with candidates.

## Functional Flows
### Registration
- Visit `/signup/`
- Choose either `Job Seeker` or `Employer`
- Employers can optionally add company information

### Authentication
- Visit `/login/` to sign in
- Visit `/logout/` to sign out

### Profile Management
- Visit `/profile/` to update profile details
- Job seekers can add a resume, skills, and work experience
- Employers can add company information and job details

### Job Posting and Search
- The home page lists active job postings
- Use search and location filters to find jobs
- Employers can create and edit jobs at `/jobs/create/`
- Employers can delete jobs from the dashboard

### Applications
- Job seekers apply from a job detail page
- Employers view applications at `/applications/`
- Job seekers can track application status from `/dashboard/`

### Messaging and Notifications
- Visit `/messages/` to view messages and send a new message
- New messages create notifications for the recipient
- Visit `/notifications/` to review updates and alerts

## System Architecture Mapping
- **Front end**: HTML, CSS, Django templates
- **Back end**: Django views, forms, models
- **Database**: SQLite via Django ORM

## Requirement Coverage
- Account creation for job seekers and employers: ✅
- Secure login/logout: ✅
- Job seeker profile creation and editing: ✅
- Employer job posting/edit/delete: ✅
- Job search and filtering: ✅
- In-platform job application submission: ✅
- Employer application review: ✅
- Messaging between users: ✅
- Notifications for applications and messages: ✅

## Notes for Reviewers
- The project uses Django's built-in authentication and secure password storage.
- The SQLite database is configured by default in `nextstepcareers/settings.py`.
- You can create an admin account with `python manage.py createsuperuser`.
