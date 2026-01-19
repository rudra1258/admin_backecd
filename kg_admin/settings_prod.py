from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    "stafflynk.in",
    "www.stafflynk.in",
    "72.61.246.114",
    "localhost",
    "127.0.0.1",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'admin_model_db',
        'USER': 'admin_user',
        'PASSWORD': 'Rudra@2003',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/home/django_user/admin_backecd/staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/django_user/admin_backecd/media'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

