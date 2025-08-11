# Overview

This is a Django-based AI image generator application that creates images from text prompts using Stable Diffusion via Hugging Face's free inference API. The application provides a user-friendly web interface for generating, viewing, downloading, and managing AI-generated images. It evolved from an initial Flask implementation with OpenAI DALL-E to the current Django implementation with Stable Diffusion to reduce costs and leverage free API usage.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
The application uses Django 5.2.5 as the primary web framework, providing a robust MVC architecture with built-in admin interface, ORM, and security features. Django was chosen over Flask for better scalability, built-in features, and user preference.

## Database Design
Uses Django ORM with a simple GeneratedImage model that stores:
- Text prompts used for generation
- Image URLs (data URLs for base64 encoded images)
- Creation timestamps
- Configured for SQLite in development and PostgreSQL in production

## Frontend Architecture
- Bootstrap 5 with Replit's dark theme for responsive UI
- Vanilla JavaScript for client-side interactions
- Font Awesome icons for visual elements
- Template-based rendering using Django's template system
- Character counting and form validation on the client side

## AI Image Generation Service
- Stable Diffusion XL via Hugging Face Inference API
- Free tier providing 30,000 characters/month (~1000 requests)
- Images generated at 1024x1024 resolution
- Built-in retry mechanism and error handling
- Negative prompts to improve image quality

## Static File Management
- Separate static and staticfiles directories
- Django's collectstatic for production deployment
- CSS and JavaScript assets organized by functionality

## URL Routing
RESTful URL patterns:
- `/` - Main generation interface
- `/generate/` - POST endpoint for image generation
- `/gallery/` - Image gallery view
- `/download/<id>/` - Image download endpoint
- `/delete/<id>/` - Image deletion endpoint

## Security Features
- CSRF protection for all forms
- Environment variable configuration for sensitive data
- Trusted origins configuration for deployment platforms
- Input validation and sanitization

# External Dependencies

## Core Framework
- Django 5.2.5 - Web framework
- python-decouple - Environment variable management

## AI Service Integration
- Hugging Face Inference API - Stable Diffusion XL model access
- Free tier: 30,000 characters/month
- Authentication via API token

## Frontend Dependencies
- Bootstrap 5 - UI framework (CDN)
- Font Awesome 6.4.0 - Icon library (CDN)
- Replit Bootstrap theme - Dark theme styling (CDN)

## Deployment Infrastructure
- Gunicorn - WSGI server for production
- Docker support - Containerization ready
- Replit platform - Development and hosting environment

## Development Tools
- Django admin interface - Content management
- Django's built-in development server
- Static file collection and management
- Database migrations system