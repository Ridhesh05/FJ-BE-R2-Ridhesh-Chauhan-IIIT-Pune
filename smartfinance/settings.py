from pathlib import Path
from datetime import timedelta
from datetime import datetime, timedelta
import os 
from django.urls import reverse_lazy
import environ

# Initialize environment variables

env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent
env.read_env(os.path.join(BASE_DIR, ".env"))


DEBUG = True
SECRET_KEY = env("SECRET_KEY")

CSRF_TRUSTED_ORIGINS = [
    "https://financebuddy-4jmq.onrender.com",
    "http://13.50.101.254:8000"
]
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'jazzmin',
    'base',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'base.middleware.RestrictAccessMiddleware',
]

ROOT_URLCONF = 'smartfinance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smartfinance.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL ='/login'
LOGIN_REDIRECT_URL = '/dashboard'

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

# env = environ.Env()
# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_API_KEY = env("SENDGRID_API_KEY", default=None)
# EMAIL_HOST = "smtp.sendgrid.net"
# EMAIL_PORT = 587  # Use 587 for TLS (recommended)
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_HOST_USER = "apikey"  # This must be exactly "apikey"

# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY  # Store this in .env for security
# DEFAULT_FROM_EMAIL = "ridheshchauhan7@gmail.com"  # Use your verified SendGrid email

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env")) 

SENDGRID_API_KEY = env("SENDGRID_API_KEY", default=None)

if not SENDGRID_API_KEY:
    raise Exception("SENDGRID_API_KEY is missing! Check your .env file or environment variables.")

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "apikey"  
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY  
DEFAULT_FROM_EMAIL = "ridheshchauhan7@gmail.com"
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

