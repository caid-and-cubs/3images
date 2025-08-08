#!/usr/bin/env python
"""Django main entry point for running the AI Image Generator."""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_generator_django.settings')
    django.setup()
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:5000'])