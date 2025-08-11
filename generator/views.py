from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from .models import GeneratedImage
import requests
import tempfile
import os
import logging
from stable_diffusion_service import get_stable_diffusion_service

logger = logging.getLogger(__name__)


def index(request):
    """Main page with image generation form"""
    return render(request, 'generator/index.html')


def generate_image(request):
    """Generate image from text prompt using Stable Diffusion"""
    if request.method != 'POST':
        return redirect('index')
    
    try:
        prompt = request.POST.get('prompt', '').strip()
        
        if not prompt:
            messages.error(request, 'Please enter a text prompt')
            return redirect('index')
        
        if len(prompt) > 1000:
            messages.error(request, 'Prompt is too long. Please keep it under 1000 characters.')
            return redirect('index')
        
        # Generate image using Stable Diffusion
        logger.info(f"Generating image for prompt: {prompt}")
        
        try:
            service = get_stable_diffusion_service()
            if not service:
                messages.error(request, 'Image generation service is not available. Please check your API key.')
                return redirect('index')
            
            image_data_url = service.generate_image(prompt)
            
            # Save to database
            new_image = GeneratedImage.objects.create(
                prompt=prompt,
                image_url=image_data_url
            )
            
            messages.success(request, 'Image generated successfully!')
            return render(request, 'generator/index.html', {
                'generated_image': image_data_url,
                'prompt': prompt,
                'image_id': new_image.id
            })
            
        except Exception as api_error:
            logger.error(f"Stable Diffusion API error: {str(api_error)}")
            
            # Check if it's an API key issue
            if "HUGGINGFACE_API_KEY" in str(api_error):
                messages.error(request, 'Hugging Face API key is required. Please add your HUGGINGFACE_API_KEY to environment variables.')
            else:
                messages.error(request, f"Error generating image: {str(api_error)}")
            
            return redirect('index')
        
    except Exception as e:
        logger.error(f"Error in generate_image: {str(e)}")
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return redirect('index')


def gallery(request):
    """Display gallery of generated images"""
    try:
        images = GeneratedImage.objects.all()[:50]  # Last 50 images
        return render(request, 'generator/gallery.html', {'images': images})
    except Exception as e:
        logger.error(f"Error in gallery: {str(e)}")
        messages.error(request, 'Error loading gallery')
        return redirect('index')


def download_image(request, image_id):
    """Download generated image"""
    import base64
    
    try:
        image = get_object_or_404(GeneratedImage, id=image_id)
        
        # Handle base64 data URLs from Stable Diffusion
        if image.image_url.startswith('data:image'):
            # Extract base64 data from data URL
            header, data = image.image_url.split(',', 1)
            image_data = base64.b64decode(data)
            
            # Generate filename
            safe_prompt = "".join(c for c in image.prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_prompt}_{image.id}.png"
            
            response = HttpResponse(image_data, content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
            
        else:
            # Handle regular URLs (fallback for legacy images)
            response = requests.get(image.image_url, timeout=30)
            response.raise_for_status()
            
            # Generate filename
            safe_prompt = "".join(c for c in image.prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_prompt}_{image.id}.png"
            
            http_response = HttpResponse(response.content, content_type='image/png')
            http_response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return http_response
        
    except Exception as e:
        logger.error(f"Error downloading image {image_id}: {str(e)}")
        messages.error(request, 'Error downloading image')
        return redirect('gallery')


def delete_image(request, image_id):
    """Delete generated image from gallery"""
    if request.method != 'POST':
        return redirect('gallery')
    
    try:
        image = get_object_or_404(GeneratedImage, id=image_id)
        image.delete()
        messages.success(request, 'Image deleted successfully')
    except Exception as e:
        logger.error(f"Error deleting image {image_id}: {str(e)}")
        messages.error(request, 'Error deleting image')
    
    return redirect('gallery')


# OpenAI function removed - now using Stable Diffusion
