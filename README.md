# Argn
This project is an end-to-end job search automation platform designed to simplify and streamline the job hunting process. It combines modern frontend technologies with a powerful backend to deliver a seamless user experience.

Key Features
User Inputs & Profile Management

Resume Upload: Users can upload their resume as a base for matching and outreach.
Custom Criteria: Input fields for domain, location, and job type help tailor the job search to individual preferences.
User Data Storage: Securely stores user emails, passwords, and resumes using Supabase.
Intelligent Job Matching

Web Scraping with BeautifulSoup (bs4): The Flask backend scrapes job listings from various sources.
ATS Scoring: Each job listing is evaluated with an ATS (Applicant Tracking System) score based on how well it matches the user's resume.
Cold Email Generation

Automatically generates personalized cold emails for proactive outreach to hiring managers, based on user inputs and resume content.
Job Alert Scheduling

Users can set up automated job alerts at their preferred frequency (daily, weekly, or monthly) to ensure they never miss new opportunities.
Technology Stack
Frontend:

TypeScript, React, Vite: Provides a fast, modern, and responsive user interface.
Backend:

Flask: Handles API requests, job scraping using BeautifulSoup, and ATS scoring logic.
Database:

Supabase: Manages secure storage of user data, including email addresses, passwords, and resumes.
Deployment:

Netlify: Hosts the frontend, ensuring high performance and scalability.
