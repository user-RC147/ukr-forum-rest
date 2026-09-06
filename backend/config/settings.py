from datetime import timedelta
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# __file__ = backend/config/settings.py
# .parent  = backend/config/
# .parent  = backend/
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

# os.getenv() always returns a string or None, and a non-empty string
# (even "False") is truthy in Python. Compare against the string directly.
DEBUG = os.getenv("DEBUG", "False") == "True"

GEO_API_URL = os.getenv("GEO_API_URL")
GEO_API_TOKEN = os.getenv("GEO_API_TOKEN")

# --- Required checks for production ---
if not DEBUG:
    if not SECRET_KEY:
        raise ImproperlyConfigured("SECRET_KEY is not set for production")

    ALLOWED_HOSTS = [
        host.strip()
        for host in os.getenv("ALLOWED_HOSTS", "").split(",")
        if host.strip()
    ]
    if not ALLOWED_HOSTS:
        raise ImproperlyConfigured("ALLOWED_HOSTS is not set for production")
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
    INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_spectacular",
    "django.contrib.postgres",
    "apps.users",
    "apps.geo",
    "apps.household",
    "apps.shop",
    "apps.files",
    "apps.search",
    "apps.articles",
]

MIDDLEWARE = [
    "config.middleware.RequestIDMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # must be above CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

AUTH_USER_MODEL = "users.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "core.users.authentication.CookieJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "core.users.csrf_permission.CsrfPermission",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "config.drf_err_handler.custom_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Ukr Forum API",
    "VERSION": "1.0.0",
}

# --- CORS ---
# Dev: Vue dev server on its own port.
# Prod: frontend and API sit behind the same nginx (same origin), but
# still read from ENV so the domain can change without rebuilding the image.
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174",
).split(",")
CORS_ALLOW_CREDENTIALS = True

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uk"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

# --- Static / media ---
# Matches nginx: location /static/ { alias /var/www/static/ },
# location /media/ { alias /var/www/media/ }, and the backend_media
# volume mounted at BASE_DIR/media in the backend/celery containers.
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Email ---
# Dev: prints to console. Prod: real SMTP if set in ENV, otherwise
# falls back to console (better than silently losing emails on a half-set config).
if not DEBUG and os.getenv("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@ukrkolo.site")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

PASSWORD_RESET_TOKEN_TTL_MINUTES = 5

# --- Cookies / HTTPS ---
# USE_HTTPS is a separate flag, not derived from DEBUG: the prod box
# currently runs over plain http (no domain/certbot yet), and a Secure
# cookie is silently dropped by the browser over http — login would break.
# Flip this to True once TLS is set up.
USE_HTTPS = os.getenv("USE_HTTPS", "False") == "True"

CSRF_COOKIE_HTTPONLY = False  # JS needs to read it (axios sends it back)
CSRF_COOKIE_SECURE = USE_HTTPS
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    if USE_HTTPS:
        SECURE_SSL_REDIRECT = False #fix 301 from healthcheck
        SECURE_HSTS_SECONDS = 31536000
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": os.getenv("SIMPLE_JWT_SIGNING_KEY") or SECRET_KEY,
    "ALGORITHM": "HS256",
    "UPDATE_LAST_LOGIN": False,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "JTI_CLAIM": "jti",
    "AUTH_COOKIE": "access_token",
    "AUTH_COOKIE_REFRESH": "refresh_token",
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_SECURE": USE_HTTPS,
    "AUTH_COOKIE_SAMESITE": "Lax" if DEBUG else "Strict",
}

# LOGIN_REDIRECT_URL = "/api/docs/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

from config.logging import BASE_LOGGING

LOGGING = BASE_LOGGING

SEARCH_HANDLERS = {
    "shop": "apps.shop.search.ProductSearchHandler",
}

# --- Sentry ---
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.2,
    send_default_pii=False,
    environment="development" if DEBUG else "production",
)

# --- Redis / Cache ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_USER_PASSWORD", "redis")
REDIS_USER = os.getenv("REDIS_USER", "redis")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_PASSWORD}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1",
    }
}

# --- Celery ---
CELERY_BROKER_URL = f"redis://{REDIS_PASSWORD}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_PASSWORD}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = os.getenv("TIMEZONE", "Europe/Berlin")
