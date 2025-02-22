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


# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = True
SECRET_KEY = env("SECRET_KEY")


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
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
    'social_django',
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
# AUTH_USER_MODEL = 'base.User'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Ensure static files are correctly configured
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Add this line to fix the error
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Folder where collected static files will be stored


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

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



# # Google OAuth Settings
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '622790057442-hv5d42ok79oi5i14lp85dj96mclsrr4r.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# AUTHENTICATION_BACKENDS = (
#     'social_core.backends.google.GoogleOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# )

# SOCIAL_AUTH_URL_NAMESPACE = 'social'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
#     'https://www.googleapis.com/auth/userinfo.email',
#     'https://www.googleapis.com/auth/userinfo.profile',
# ]

# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'dashboard'
# LOGOUT_URL = 'logout'
# LOGOUT_REDIRECT_URL = 'login'

# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.auth_allowed',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.user.get_username',
#     'social_core.pipeline.social_auth.associate_by_email',
#     'social_core.pipeline.user.create_user',
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
#     'base.pipeline.create_user_profile',  # Your custom pipeline
# )