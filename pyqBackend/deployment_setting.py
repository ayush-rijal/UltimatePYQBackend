import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ.get['RENDER_EXTERNAL_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ.get['RENDER_EXTERNAL_HOSTNAME']]

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!@#qwertyuiopasdfghjklzxcvbnm1234567890')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# FORNTED URL ARE UPDATED
# CORS_ALLOWED_ORIGINS = getenv(
#     'CORS_ALLOWED_ORIGINS',
#     'http://localhost:3000,http://127.0.0.1:3000'
# ).split(',')


STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}


DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}

