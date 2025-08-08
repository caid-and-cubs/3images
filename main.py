# Django WSGI entry point for Gunicorn
import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_generator_django.settings')
django.setup()

app = get_wsgi_application()
