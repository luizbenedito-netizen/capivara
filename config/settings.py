""" Django 5.2.6. """

import os
from pathlib import Path
import dj_database_url
from decouple import config
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h_@q^*@4^u_nmphi46)72m)lpvx5+mb7im9=oe=xd_oa#=zti2'

# SECURITY WARNING: don't run with debug turned on in production!
from decouple import config

DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

HOSTNAME = os.environ.get('HOSTNAME', '').strip()

if DEBUG:
    SITE_HOST = HOSTNAME if HOSTNAME else 'localhost'
    SITE_PROTOCOL = 'http'

    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    if HOSTNAME:
        ALLOWED_HOSTS.append(HOSTNAME)

    CSRF_TRUSTED_ORIGINS = [
        f'{SITE_PROTOCOL}://127.0.0.1:8000',
        f'{SITE_PROTOCOL}://localhost:8000',
    ]
    if HOSTNAME:
        CSRF_TRUSTED_ORIGINS.append(f'{SITE_PROTOCOL}://{HOSTNAME}')

    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

else:
    SITE_HOST = HOSTNAME
    SITE_PROTOCOL = 'https'

    ALLOWED_HOSTS = [HOSTNAME]
    CSRF_TRUSTED_ORIGINS = [f'{SITE_PROTOCOL}://{HOSTNAME}']

    SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Application definition

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_vite',
    'django_vite_plugin'
]

LOCAL_APPS = [
    'app'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DJANGO_VITE = {
    "default": {
        "dev_mode": False,
        "manifest_path": BASE_DIR / "static" / ".vite" / "manifest.json",
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.globals.cache'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '123456'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# Segurança de cookies / sessão
# SESSION_COOKIE_SECURE = True # apenas via HTTPS
# CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False # normalmente False para compatibilidade com JS (ok)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

# Headers de segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True            # forçar HTTPS no deploy (apenas se app servir HTTPS)
X_FRAME_OPTIONS = 'DENY'


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Settings
FERNET_KEY = os.environ.get('RECOVERY_KEY', default='rBN6BbCiPXXgm9x5COeB0EF6To9LtimLwHKgLf0LbCI=')
RECOVERY_TIME_SECONDS = os.environ.get('RECOVERY_TIME_SECONDS', default='3600')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('RECOVERY_EMAIL_ACCOUNT', default='')
EMAIL_HOST_PASSWORD = os.environ.get('RECOVERY_EMAIL_PASSWORD', default='')
