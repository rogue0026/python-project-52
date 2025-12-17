import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'task_manager/templates')
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(os.getenv("DEBUG"))
LOGIN_URL = 'login_view'
LOGIN_REDIRECT_URL = 'start_page'
LOGOUT_REDIRECT_URL = 'start_page'
ROOT_URLCONF = 'task_manager.urls'
WSGI_APPLICATION = 'task_manager.wsgi.application'
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_HOSTS = [
    'task-manager-ekb1.onrender.com',
    'webserver',
    'localhost',
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_bootstrap5',
    'django_filters',

    'task_manager',
    'task_manager.users',
    'task_manager.statuses',
    'task_manager.tasks',
    'task_manager.labels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROLLBAR = {
    'access_token': os.getenv("ROLLBAR_TOKEN"),
    'environment': 'development' if os.getenv('DEBUG') == "on" else 'production',
    'code_version': '1.0',
    'branch': 'main',
    'root': BASE_DIR,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': dj_database_url.parse(os.getenv("DATABASE_URL"))
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            "min_length": 3,
        }
    },
]