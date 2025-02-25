"""
WSGI config for news_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_web.settings')

application = get_wsgi_application()


WSGI_APPLICATION = 'news_web.wsgi.application'

# Ensure the news_web directory is in the Python path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Double-check that the wsgi.py file exists in the news_web directory
wsgi_path = os.path.join(BASE_DIR, 'news_web', 'wsgi.py')
if not os.path.exists(wsgi_path):
    raise ImproperlyConfigured(f"WSGI file not found: {wsgi_path}")

# Verify that the wsgi.py file contains the 'application' object
try:
    from news_web.wsgi import application
except ImportError:
    raise ImproperlyConfigured("Unable to import 'application' from news_web.wsgi")