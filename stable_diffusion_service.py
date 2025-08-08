"""
Stable Diffusion API service using Hugging Face Inference API
Free tier: 30,000 characters/month, ~1000 requests/month
"""
import os
import requests
import time
import base64
from io import BytesIO
from django.conf import settings


class StableDiffusionService:
    def __init__(self):
        # Hugging Face API settings
        self.hf_api_key = os.environ.get("HUGGINGFACE_API_KEY")
        # Using SDXL for better quality images
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        
    def generate_image(self, prompt, max_retries=3):
        """
        Generate an image from a text prompt using Stable Diffusion
        Returns the image as base64 encoded data URL
        """
        if not self.hf_api_key:
            raise Exception("HUGGINGFACE_API_KEY environment variable is required")
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "blurry, bad quality, distorted, ugly, deformed",
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "width": 1024,
                "height": 1024
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    # Convert response to base64 data URL
                    image_bytes = response.content
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')
                    data_url = f"data:image/png;base64,{base64_image}"
                    return data_url
                
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    error_data = response.json()
                    estimated_time = error_data.get('estimated_time', 20)
                    print(f"Model loading, waiting {estimated_time} seconds...")
                    time.sleep(min(estimated_time, 30))  # Cap wait time at 30 seconds
                    continue
                
                else:
                    # Other error
                    error_msg = f"API error: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('error', 'Unknown error')}"
                    except:
                        error_msg += f" - {response.text}"
                    
                    if attempt == max_retries - 1:
                        raise Exception(error_msg)
                    else:
                        print(f"Attempt {attempt + 1} failed: {error_msg}")
                        time.sleep(2 ** attempt)  # Exponential backoff
                        
            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    raise Exception("Request timed out. The model might be busy.")
                time.sleep(5)
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Network error: {str(e)}")
                time.sleep(2)
        
        raise Exception("Failed to generate image after multiple attempts")


# Global instance
stable_diffusion_service = StableDiffusionService()