# AI Image Generator with Stable Diffusion

A Django-based web application that generates images from text prompts using Stable Diffusion via Hugging Face's free API.

## Features

- 🎨 Generate images from text descriptions using Stable Diffusion
- 🖼️ Image gallery to view all generated images
- 💾 Download generated images
- 🗑️ Delete images from gallery
- 📱 Responsive design with Bootstrap
- 🆓 Completely free using Hugging Face API (30,000 characters/month)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/caid-and-cubs/3images.git
cd 3images
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Hugging Face API Key
1. Go to https://huggingface.co and create a free account
2. Go to Settings → Access Tokens
3. Create a new token with "Read" permissions
4. Copy the token that starts with "hf_"

### 4. Set Environment Variables
Create a `.env` file or set environment variables:
```bash
export HUGGINGFACE_API_KEY=your_huggingface_api_key_here
export DJANGO_SECRET_KEY=your_secret_key_here
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Application
```bash
python manage.py runserver 0.0.0.0:5000
```

## API Usage

The application uses Stable Diffusion XL Base 1.0 through Hugging Face's Inference API, which provides:
- Free tier: 30,000 characters/month (~1000+ images)
- High-quality 1024x1024 images
- No API costs

## Project Structure

```
├── generator/                 # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── urls.py               # URL routing
│   └── migrations/           # Database migrations
├── django_templates/         # HTML templates
├── static/                   # Static files (CSS, JS)
├── stable_diffusion_service.py # Stable Diffusion API service
├── manage.py                 # Django management script
└── main.py                   # WSGI entry point
```

## Recent Updates

- ✅ Migrated from Flask to Django
- ✅ Switched from OpenAI DALL-E to free Stable Diffusion
- ✅ Updated image handling for base64 data URLs
- ✅ Added proper error handling and user feedback
- ✅ Maintained all original functionality while eliminating API costs

## Docker Deployment

### Quick Start with Docker Compose

1. **Clone the repository**:
```bash
git clone https://github.com/caid-and-cubs/3images.git
cd 3images
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env file and add your HUGGINGFACE_API_KEY
```

3. **Build and run with Docker Compose**:
```bash
docker-compose up --build
```

4. **Access the application**:
Open http://localhost:8000 in your browser

### Manual Docker Build

```bash
# Build the Docker image
docker build -t ai-image-generator .

# Run the container
docker run -p 8000:8000 \
  -e HUGGINGFACE_API_KEY=your_api_key_here \
  -e DJANGO_SECRET_KEY=your_secret_key_here \
  ai-image-generator
```

### Production Deployment

For production deployment:

1. **Use PostgreSQL instead of SQLite**:
   - Uncomment the PostgreSQL service in `docker-compose.yml`
   - Update the `DATABASE_URL` environment variable

2. **Set secure environment variables**:
   - Generate a strong `DJANGO_SECRET_KEY`
   - Set `DEBUG=False`
   - Configure proper domain in Django settings

3. **Use a reverse proxy** (Nginx/Apache) for serving static files and SSL termination

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HUGGINGFACE_API_KEY` | Yes | Your Hugging Face API token |
| `DJANGO_SECRET_KEY` | Yes | Django secret key for security |
| `DEBUG` | No | Set to `False` for production (default: True) |
| `DATABASE_URL` | No | PostgreSQL URL (default: SQLite) |

## License

This project is open source and available under the MIT License.