"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from os import path
from pathlib import Path
from corsheaders.defaults import default_headers
from datetime import timedelta
from environs import Env, EnvError


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'users.User'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1e1s-xppujqf)_f7l_)o7*uqs7ifdolujwtu7c!x=6&5(cq+0v'

env = Env()
env.read_env(path.join(BASE_DIR, ".env"), recurse=False)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1:6379/0', '127.0.0.1:8088']

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
    CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8088", "http://0.0.0.0:8088", "http://localhost:8088"]
    CSRF_TRUSTED_ORIGINS += env.list("CSRF_TRUSTED_ORIGINS", [])

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    #Useful Models
    'polymorphic',
    'django_filters',
    'django_drf_filepond',
    'django_celery_results',
    
    #Authentication
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_nested',
    'rest_auth',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.sites',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #apps
    'users',
    'roles',
    'projects',
    'corsheaders',
    'data_export',
    'data_import',
    'examples',
    'label_types',
    'labels'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    #Main
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

# Role settings
ROLE_PROJECT_ADMIN = env("ROLE_PROJECT_ADMIN", "project_admin")
ROLE_ANNOTATOR = env("ROLE_ANNOTATOR", "annotator")
ROLE_ANNOTATION_APPROVER = env("ROLE_ANNOTATION_APPROVER", "annotation_approver")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'


#rest framework key for JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    # Other settings...
}


# File upload setting
MAX_UPLOAD_SIZE = env.int("MAX_UPLOAD_SIZE", pow(1024, 3))  # default: 1GB per a file
ENABLE_FILE_TYPE_CHECK = env.bool("ENABLE_FILE_TYPE_CHECK", False)
IMPORT_BATCH_SIZE = env.int("IMPORT_BATCH_SIZE", 1000)


# User media files
MEDIA_ROOT = env("MEDIA_ROOT", path.join(BASE_DIR, "media"))
MEDIA_URL = "/media/"


# Filepond settings
DJANGO_DRF_FILEPOND_UPLOAD_TMP = path.join(BASE_DIR, "filepond-temp-uploads")
DJANGO_DRF_FILEPOND_FILE_STORE_PATH = MEDIA_ROOT




# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'text_annotation',
        'USER': 'postgres',
        'PASSWORD': 'biologyc4',
        'HOST': '127.0.0.1',  # Or 'localhost'
        'PORT': '5432',
    }
    
}


# Celery settings
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

APPEND_SLASH = False

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8088",
    "http://127.0.0.1:8088",
]


# Specify which methods are allowed
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_HEADERS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'upload-length', 
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=23),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=3),


    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
