"""
Django settings for Usbot project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3$-)&3ao8*jf$l6y$=f%fm8$u!sxwbv1#2e8cu@ns+20glsj*6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['3.108.11.221', 'localhost']


# Application definition

INSTALLED_APPS = [
    #'jazzmin',
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'Store',
    'wishlist',
    'ckeditor',
    'ckeditor_uploader',
    'easy_thumbnails',
    'image_cropping',
    

    
  
    
    
    # paypal intergration
    # 'paypal.standard.ipn',
]


IMAGE_CROPPING_BACKEND = 'image_cropping.backends.easy_thumbs.EasyThumbnailsBackend'
IMAGE_CROPPING_BACKEND_PARAMS = {}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Usbot.urls'

NPM_BIN_PATH = "/path/to/npm"

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
                'Store.context_processors.custom_admin_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'Usbot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'USBOT', 
        'USER': 'ammu',
        'PASSWORD': '123',
        'HOST': 'localhost', 
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'




# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
INTERNAL_IPS = [
    "127.0.0.1",
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



# This is the directory where collectstatic will copy all your static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# This is the URL prefix used when referring to static files (CSS, JavaScript, images, etc.).
STATIC_URL = '/static/'
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
TAILWIND_APP_NAME = 'theme'


AUTH_USER_MODEL = 'Store.UserProfile'


# Email Verification

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER='usbotbottle@gmail.com'
EMAIL_HOST_PASSWORD='amny bqog bjyy ozmu'
DEFAULT_FROM_EMAIL='usbotbottle@gmail.com'





CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js'  # You can change this URL if needed
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'default':{
        'skin': 'moono',
        'codeSnippet_theme': 'monokai',
        'toolbar': 'all',
        'extraPlugins': ','.join(
            [
                'codesnippet',
                'widget',
                'dialog'
            ]
        ),
    }
    
    
}

KEY = 'rzp_test_HIRhNkqNybeWdx'
SECRET = 'SbAXrEwCX45PooisjDgRmJ2x'



STRIPE_SECRET_KEY = "sk_test_51OeX1WSJJpJuUlr4Qhh0BfM5SWtxYnJlF5xelbG2qRG8O7L6FObTFmQ8Td4ZLs1VbCENJilbj4VvfrhjyuJn20QP00J1izk0KV"
STRIPE_PUBLISHABLE_KEY = "pk_test_51OeX1WSJJpJuUlr4uWV5k5OgBy8nsFdTUy8oi5vaORefISDATgo8zKKDWcA5S22i4Ky8Dr8Rq5WK5alfDb5CD5h600Kbn29miS"

# PAYPAL_RECEIVER_EMAIL = 'usbotbottle@gmail.com'
# PAYPAL_TEST = True
