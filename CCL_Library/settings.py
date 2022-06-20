from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

ALLOWED_HOSTS = ['https://ccl-library-u9m5e.ondigitalocean.app/', 'https://cosmicchrist.love/']

CSRF_TRUSTED_ORIGINS = ['https://ccl-library-u9m5e.ondigitalocean.app/', 'https://*.127.0.0.1', 'https://*.ondigitalocean.app','https://cosmicchrist.love/']

INSTALLED_APPS = [
    'library.apps.LibraryConfig',
    'users.apps.UsersConfig',
    'home.apps.HomeConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'phone_field',
    'tinymce',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CCL_Library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'CCL_Library.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),

    }
}


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# STATIC_URL = 'static/'
STATIC_URL = 'https://ega.s3.us-east-2.amazonaws.com/ccl-library-static/'
# STATIC_URL = 'https://django-whurthy.s3.us-west-1.amazonaws.com/whurthy-static/'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'mail.tsiworks.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
FROM_EMAIL = os.environ.get('FROM_EMAIL')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')

COMPANY_NAME = os.environ.get('COMPANY_NAME')
DOMAIN  = os.environ.get('WHURTHY_DOMAIN')

TINY_API = os.environ.get('TINY_API')
# TINY_JWK = os.environ.get('TINY_JWK')

# TINYMCE_JS_URL = TINY_API
# TINYMCE_JS_ROOT = 'https://ega.s3.us-east-2.amazonaws.com/ccl-library-static/'

TINYMCE_DEFAULT_CONFIG = {
    "height": "330px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "tinydrive advlist autolink lists link image charmap print preview anchor searchreplace visualblocks "
    "fullscreen insertdatetime media table paste code help wordcount",
    "toolbar": "undo redo | bold italic underline strikethrough | formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist "
    "casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}
    # "tinydrive_token_provider": f'{TINY_API}',
    # "tinydrive_dropbox_app_key": '',
    # "tinydrive_upload_path": '/library/uploads',
    # "tinydrive_max_image_dimension": 2048,

