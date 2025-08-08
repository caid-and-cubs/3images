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
from openai import OpenAI

# Initialize OpenAI client
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

logger = logging.getLogger(__name__)


def index(request):
    """Main page with image generation form"""
    return render(request, 'generator/index.html')


def generate_image(request):
    """Generate image from text prompt"""
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
        
        # Generate image using OpenAI DALL-E
        logger.info(f"Generating image for prompt: {prompt}")
        result = generate_image_with_dalle(prompt)
        
        if 'error' in result:
            messages.error(request, f'Error generating image: {result["error"]}')
            return redirect('index')
        
        # Save to database
        new_image = GeneratedImage.objects.create(
            prompt=prompt,
            image_url=result['url']
        )
        
        messages.success(request, 'Image generated successfully!')
        return render(request, 'generator/index.html', {
            'generated_image': result['url'],
            'prompt': prompt,
            'image_id': new_image.id
        })
        
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
    try:
        image = get_object_or_404(GeneratedImage, id=image_id)
        
        # Download image from URL
        response = requests.get(image.image_url, timeout=30)
        response.raise_for_status()
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.write(response.content)
        temp_file.close()
        
        # Generate filename
        safe_prompt = "".join(c for c in image.prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_prompt}_{image.id}.png"
        
        # Read file and return as response
        with open(temp_file.name, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
        # Clean up temp file
        os.unlink(temp_file.name)
        
        return response
        
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


def generate_image_with_dalle(prompt):
    """
    Generate image using OpenAI DALL-E 3
    
    Args:
        prompt (str): Text description for image generation
        
    Returns:
        dict: Contains 'url' on success or 'error' on failure
    """
    try:
        if not openai_client:
            return {"error": "OpenAI API key not configured"}
        
        if not prompt or len(prompt.strip()) == 0:
            return {"error": "Prompt cannot be empty"}
        
        # Clean and validate prompt
        prompt = prompt.strip()
        if len(prompt) > 1000:
            return {"error": "Prompt is too long (max 1000 characters)"}
        
        logger.info(f"Generating image with DALL-E 3 for prompt: {prompt[:100]}...")
        
        # the newest OpenAI model is "dall-e-3" for image generation
        # do not change this unless explicitly requested by the user
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard",
            response_format="url"
        )
        
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            logger.info(f"Image generated successfully: {image_url}")
            return {"url": image_url}
        else:
            logger.error("No image data returned from OpenAI")
            return {"error": "No image was generated"}
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error generating image: {error_msg}")
        
        # Handle specific OpenAI errors
        if "content_policy_violation" in error_msg.lower():
            return {"error": "Content violates OpenAI's usage policies. Please try a different prompt."}
        elif "insufficient_quota" in error_msg.lower() or "quota" in error_msg.lower():
            return {"error": "API quota exceeded. Please try again later."}
        elif "invalid_api_key" in error_msg.lower():
            return {"error": "Invalid API key configuration."}
        elif "rate_limit" in error_msg.lower():
            return {"error": "Rate limit exceeded. Please wait a moment and try again."}
        elif "billing_hard_limit_reached" in error_msg.lower():
            return {"error": "Billing limit reached. Please check your OpenAI account."}
        else:
            return {"error": f"Failed to generate image: {error_msg}"}
