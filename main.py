"""
Point d'entrée WSGI pour l'application Django de génération d'images IA
"""
import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Ajouter le répertoire du projet au PATH Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_generator_django.settings')

# Initialisation de Django
django.setup()

# Application WSGI pour Gunicorn
app = get_wsgi_application()