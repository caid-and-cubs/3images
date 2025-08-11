# Overview

This is a Django-based web application that generates images from text prompts using AI. The application utilizes Stable Diffusion through Hugging Face's free Inference API to create images based on user descriptions. Users can generate images, view them in a gallery, download them, and manage their collection through a clean, responsive web interface.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **Django 5.2.5**: Main web framework providing MVC architecture, ORM, admin interface, and URL routing
- **Python**: Core programming language with modern async/await patterns
- **SQLite**: Default database for development (can be upgraded to PostgreSQL for production)

## AI Image Generation Service
- **Stable Diffusion XL**: Primary AI model accessed via Hugging Face Inference API
- **Service Layer**: Custom `StableDiffusionService` class that handles API communication, prompt enhancement, and image processing
- **Base64 Data URLs**: Images are stored as data URLs in the database for simplicity and self-containment

## Data Models
- **GeneratedImage Model**: Stores image metadata including prompt text, image data URL, and creation timestamp
- **Django ORM**: Handles database operations with built-in migrations and admin interface integration

## Frontend Architecture
- **Server-Side Rendering**: Django templates with Jinja2-style templating
- **Bootstrap 5**: UI framework with dark theme from Replit's CDN
- **Responsive Design**: Mobile-first approach with responsive grid system
- **Progressive Enhancement**: JavaScript adds interactive features like character counting and loading states

## Static Asset Management
- **Django's Static Files**: Handles CSS, JavaScript, and other static assets
- **CDN Integration**: Bootstrap and Font Awesome loaded from CDNs for better performance
- **Custom Styling**: Application-specific styles for image galleries and loading animations

## Configuration Management
- **Environment Variables**: Sensitive data like API keys managed through environment variables
- **Django Settings**: Centralized configuration with separate settings for development and production
- **CSRF Protection**: Built-in security features with trusted origins for deployment platforms

# External Dependencies

## AI Services
- **Hugging Face Inference API**: Free tier providing 30,000 characters/month for Stable Diffusion image generation
- **Stable Diffusion XL Base 1.0**: Specific model endpoint for high-quality image generation

## Frontend Libraries
- **Bootstrap 5**: CSS framework loaded from Replit's CDN with dark theme
- **Font Awesome 6.4.0**: Icon library for UI elements and visual indicators
- **jQuery**: JavaScript library included with Django admin for enhanced interactions

## Python Packages
- **Django**: Web framework with built-in ORM, admin, and security features
- **python-decouple**: Environment variable management for secure configuration
- **Pillow**: Image processing library for handling generated images
- **requests**: HTTP client library for API communication with Hugging Face

## Development Tools
- **Django Admin**: Built-in administrative interface for managing generated images
- **Django's Development Server**: Built-in server for local development and testing
- **Static File Handling**: Django's collectstatic for production deployment

## Deployment Considerations
- **WSGI Compatibility**: Configured for deployment on platforms like Replit, Heroku, or traditional servers
- **CORS Settings**: Configured for cross-origin requests in development environments
- **Database Flexibility**: Designed to work with SQLite for development and PostgreSQL for production scaling