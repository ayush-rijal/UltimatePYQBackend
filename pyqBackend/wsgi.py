"""
WSGI config for pyqBackend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

setting_module = 'pyqBackend.deployment_setting' if os.environ.get('RENDER_EXTERNAL_HOSTNAME') else 'pyqBackend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyqBackend.settings')

application = get_wsgi_application()
