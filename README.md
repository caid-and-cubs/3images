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

## License

This project is open source and available under the MIT License.