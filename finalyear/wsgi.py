"""
WSGI config for finalyear project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from footcount import views

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finalyear.settings")

application = get_wsgi_application()
# views.test_function()