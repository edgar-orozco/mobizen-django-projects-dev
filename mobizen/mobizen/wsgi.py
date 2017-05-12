"""
WSGI config for mobizen project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import sys
sys.path.append('/home/django/django-projects/mobizen/')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mobizen.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import djcelery
djcelery.setup_loader()
