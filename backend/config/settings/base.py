import os
from pathlib import Path

from dotenv import load_dotenv
from datetime import timedelta

# BASE_DIR вказує на папку backend/
# __file__ = backend/config/settings/base.py
# .parent   = backend/config/settings/
# .parent   = backend/config/
# .parent   = backend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Завантажуємо .env з папки backend/
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

# Geo API
GEO_API_URL = os.getenv("GEO_API_URL")
GEO_API_TOKEN = os.getenv("GEO_API_TOKEN")

ALLOWED_HOSTS = []   #["127.0.0.1", "localhost"]

# --- Додатки ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_spectacular",
    'django.contrib.postgres',
    # Local
    "apps.users",
    "apps.geo",
    "apps.household",
    "apps.shop",
    "apps.files",
    "apps.search",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # ← вище CommonMiddleware!
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- База даних (PostgreSQL) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# --- Кастомна модель користувача ---
# Django повинен знати що замість вбудованого User використовуємо свій
AUTH_USER_MODEL = "users.CustomUser"
# AUTH_USER_MODEL = 'apps_users.CustomUser'

# --- DRF + JWT ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        #"rest_framework_simplejwt.authentication.JWTAuthentication",
        'apps.users.api.jwt.authentication.CookieJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',        # САМЕ ДЛЯ api-auth/login/
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# DEFAULT_PERMISSION_CLASSES=[
#     'rest_framework.permissions.IsAuthenticated',
# ]

# --- OpenAPI документація (drf-spectacular) ---
SPECTACULAR_SETTINGS = {
    "TITLE": "Ukr Forum API",
    "VERSION": "1.0.0",
}

# --- CORS ---
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vue dev server
    "http://localhost:5174",
]
CORS_ALLOW_CREDENTIALS = True

# --- Паролі ---
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Мова і час ---
LANGUAGE_CODE = "uk"  # українська
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

# --- Статика ---
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Email ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # в dev — виводить email в термінал
DEFAULT_FROM_EMAIL = "noreply@ukr-forum.com"

# --- Frontend URL (для посилань в email) ---
FRONTEND_URL = "http://localhost:5173"

# --- Serving files uploaded---
MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')  # или где у тебя файлы


SIMPLE_JWT = {
    # Змінюємо час дії основного токена на 24 години (1 день)
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    # Refresh токен зазвичай роблять довшим (наприклад, 7 днів),
    # щоб користувач не переавторизовувався щодня
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # Решта ваших поточних налаштувань SIMPLE_JWT (якщо вони є)
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),

    # httpOnly cookies
    "AUTH_COOKIE": "access_token",
    "AUTH_COOKIE_REFRESH": "refresh_token",
    "AUTH_COOKIE_HTTP_ONLY": True, 
}






# Куди перенаправляти користувача після успішного входу
#LOGIN_REDIRECT_URL = "/api/docs/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# --- Logger conf---
from apps.files.logging import LOGGING as FILES_LOGGING
from apps.shop.logging import LOGGING as SHOP_LOGGING
from apps.search.logging import LOGGING as SEARCH_LOGGING
from apps.geo.logging import LOGGING as GEO_LOGGING
from config.logging import merge_logging_configs

LOGGING = merge_logging_configs(SHOP_LOGGING, FILES_LOGGING, SEARCH_LOGGING, GEO_LOGGING)

# --- Modules for search---
SEARCH_HANDLERS = {
    "shop": "apps.shop.search.ProductSearchHandler",
}
