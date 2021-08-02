from pathlib import Path
from datetime import timedelta
from decouple import config , Csv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    # 'whitenoise.runserver_nostatic',# whitenoise
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ####### My Apps #######
    # drf
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    'accounts',
    'product',
    'shopping',
    'panel',

    ####### Additional Apps ####### 
    'django_cleanup.apps.CleanupConfig', # clear (Automatically clear image file after delete) :
    # document 
    'drf_yasg',
]

MIDDLEWARE = [
    # New Middleware :
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware', # whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

####### Cors settings ####### (It will change later  !!)
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'Sakura.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Sakura.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': config('ENGINE',default="django.db.backends.sqlite3"),
        'NAME': config('NAME',default=BASE_DIR / 'db.sqlite3'),
        'USER': config('USER',default=""),
        'PASSWORD':config('PASSWORD',default=""),
        'HOST': config('HOST',default=""),
        'PORT': config('PORT',default="")
    }
}

# DRF Config
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # Test section : 
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ],
}

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# django-rest-framework-simplejwt :
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=3),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=5),
}

# Email config
EMAIL_BACKEND = config('EMAIL_BACKEND' , default='django.core.mail.backends.console.EmailBackend')
EMAIL_USE_TLS = config('EMAIL_USE_TLS' , cast=bool , default=True)
EMAIL_HOST = config('EMAIL_HOST', default="EMAIL_HOST")
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default="EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default="EMAIL_HOST_PASSWORD")
EMAIL_PORT = config('EMAIL_PORT' , cast=int, default=587)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

## Arrange files
STATIC_URL = '/static/'
MEDIA_URL = "/media/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR , 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR , "staticfiles")
MEDIA_ROOT   = os.path.join(BASE_DIR , "media")

# origin site url :
SITE_URL=config('SITE_URL')