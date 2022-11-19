"""
WSGI config for DOGGO_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import os
import sys

path = '/home/choko69/Desktop/Projects/DOGGO/DOGGO_backend/'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DOGGO_backend.settings')

application = get_wsgi_application()
