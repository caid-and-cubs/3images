"""
Service pour la génération d'images avec Stable Diffusion via Hugging Face
"""
import os
import requests
import base64
from io import BytesIO
from PIL import Image
import time


# Instance globale du service
stable_diffusion_service = None

def get_stable_diffusion_service():
    """Retourne l'instance du service Stable Diffusion"""
    global stable_diffusion_service
    if stable_diffusion_service is None:
        stable_diffusion_service = StableDiffusionService()
    return stable_diffusion_service

class StableDiffusionService:
    def __init__(self):
        self.api_key = os.environ.get('HUGGINGFACE_API_KEY')
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY environment variable is required")
        
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
    
    def generate_image(self, prompt, negative_prompt=None, width=1024, height=1024):
        """
        Génère une image à partir d'un prompt texte
        
        Args:
            prompt (str): Description de l'image à générer
            negative_prompt (str): Éléments à éviter dans l'image
            width (int): Largeur de l'image (par défaut 1024)
            height (int): Hauteur de l'image (par défaut 1024)
        
        Returns:
            str: Image en base64 data URL ou None en cas d'erreur
        """
        try:
            # Amélioration du prompt avec des mots-clés de qualité
            enhanced_prompt = f"{prompt}, high quality, detailed, professional, 8k resolution"
            
            # Prompt négatif par défaut pour améliorer la qualité
            default_negative = "blurry, low quality, distorted, deformed, ugly, bad anatomy, bad proportions"
            if negative_prompt:
                full_negative_prompt = f"{negative_prompt}, {default_negative}"
            else:
                full_negative_prompt = default_negative
            
            payload = {
                "inputs": enhanced_prompt,
                "parameters": {
                    "negative_prompt": full_negative_prompt,
                    "width": width,
                    "height": height,
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5
                }
            }
            
            # Tentative de génération avec retry
            for attempt in range(3):
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    # Conversion de l'image en base64
                    image_bytes = response.content
                    image = Image.open(BytesIO(image_bytes))
                    
                    # Conversion en base64 pour stockage dans la base de données
                    buffered = BytesIO()
                    image.save(buffered, format="PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode()
                    
                    return f"data:image/png;base64,{img_base64}"
                
                elif response.status_code == 503:
                    # Modèle en cours de chargement, on attend
                    error_data = response.json()
                    if "estimated_time" in error_data:
                        wait_time = min(error_data["estimated_time"], 30)
                        print(f"Modèle en chargement, attente de {wait_time} secondes...")
                        time.sleep(wait_time)
                        continue
                    else:
                        time.sleep(10)  # Attente par défaut
                        continue
                
                else:
                    print(f"Erreur API Hugging Face: {response.status_code} - {response.text}")
                    if attempt < 2:  # Retry pour les autres erreurs
                        time.sleep(5)
                        continue
                    break
            
            return None
            
        except requests.exceptions.Timeout:
            print("Timeout lors de la génération d'image")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête: {e}")
            return None
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            return None
    
    def is_available(self):
        """
        Vérifie si le service est disponible
        
        Returns:
            bool: True si le service est disponible
        """
        try:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                timeout=10
            )
            return response.status_code in [200, 503]  # 503 = modèle en chargement
        except:
            return False


# Initialisation de l'instance globale
try:
    stable_diffusion_service = StableDiffusionService()
except:
    stable_diffusion_service = None