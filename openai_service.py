import os
import logging
from openai import OpenAI

# Get API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logging.warning("OPENAI_API_KEY not found in environment variables")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

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
        
        logging.info(f"Generating image with DALL-E 3 for prompt: {prompt[:100]}...")
        
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
            logging.info(f"Image generated successfully: {image_url}")
            return {"url": image_url}
        else:
            logging.error("No image data returned from OpenAI")
            return {"error": "No image was generated"}
            
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error generating image: {error_msg}")
        
        # Handle specific OpenAI errors
        if "content_policy_violation" in error_msg.lower():
            return {"error": "Content violates OpenAI's usage policies. Please try a different prompt."}
        elif "insufficient_quota" in error_msg.lower() or "quota" in error_msg.lower():
            return {"error": "API quota exceeded. Please try again later."}
        elif "invalid_api_key" in error_msg.lower():
            return {"error": "Invalid API key configuration."}
        elif "rate_limit" in error_msg.lower():
            return {"error": "Rate limit exceeded. Please wait a moment and try again."}
        else:
            return {"error": f"Failed to generate image: {error_msg}"}
