# AI Image Generator

## Overview

This is a Django-based web application that generates images from text prompts using Stable Diffusion via Hugging Face's free API. Users can input text descriptions and receive AI-generated images, which are stored in a database and displayed in a gallery. The application features a modern dark-themed interface with Bootstrap styling and provides functionality for viewing, downloading, and managing generated images.

**Recent Changes:** 
- Successfully migrated from Flask to Django on August 8, 2025
- Switched from OpenAI's DALL-E API to free Stable Diffusion via Hugging Face API
- Updated image handling to work with base64 data URLs instead of external URLs
- Maintained all original functionality while eliminating API costs

## User Preferences

Preferred communication style: Simple, everyday language.
Preferred framework: Django (migrated from Flask)

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with dark theme from Replit's CDN for consistent styling
- **Client-side Logic**: Vanilla JavaScript for form handling, character counting, and gallery interactions
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

### Backend Architecture
- **Web Framework**: Flask with modular structure separating concerns
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension for database operations
- **Model Layer**: Single `GeneratedImage` model storing prompts, image URLs, and timestamps
- **Service Layer**: Dedicated `openai_service.py` module for DALL-E 3 integration
- **Configuration**: Environment-based configuration for database URLs and API keys

### Data Storage
- **Primary Database**: Configurable between SQLite (development) and PostgreSQL (production) via `DATABASE_URL` environment variable
- **Schema Design**: Simple single-table design with auto-incrementing IDs, text prompts, image URLs, and creation timestamps
- **Connection Management**: Pool recycling and pre-ping enabled for production reliability

### Authentication and Authorization
- **Session Management**: Flask's built-in session handling with configurable secret key
- **Security**: No user authentication implemented - application is open access
- **CSRF Protection**: Not currently implemented

## External Dependencies

### APIs and Services
- **OpenAI DALL-E 3**: Primary image generation service requiring `OPENAI_API_KEY` environment variable
- **Image Hosting**: Generated images are hosted by OpenAI's CDN, URLs stored in database

### Third-party Libraries
- **Flask Ecosystem**: Core framework with SQLAlchemy, Jinja2 templating
- **Bootstrap 5**: UI framework loaded from Replit's CDN with dark theme
- **Font Awesome 6.4.0**: Icon library loaded from CDN for UI elements
- **Werkzeug ProxyFix**: Middleware for handling proxy headers in deployment

### Infrastructure Requirements
- **Database**: SQLite for development, PostgreSQL recommended for production
- **Environment Variables**: `OPENAI_API_KEY` (required), `DATABASE_URL` (optional), `SESSION_SECRET` (optional)
- **Python Dependencies**: Flask, SQLAlchemy, OpenAI client library, Requests for HTTP operations

### Deployment Considerations
- **WSGI Application**: Configured with ProxyFix for reverse proxy deployment
- **Static Assets**: Served through Flask's static file handling
- **Database Migrations**: Auto-creation on startup, no formal migration system implemented