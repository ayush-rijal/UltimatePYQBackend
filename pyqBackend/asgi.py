"""
ASGI config for pyqBackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
setting_module = 'pyqBackend.deployment_setting' if os.environ.get('RENDER_EXTERNAL_HOSTNAME') else 'pyqBackend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyqBackend.settings')

application = get_asgi_application()
