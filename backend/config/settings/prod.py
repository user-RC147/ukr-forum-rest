from .base import *

DEBUG = False

# На продакшні треба вказати реальний домен
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Безпека
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


SIMPLE_JWT |= {
    "AUTH_COOKIE_SECURE": True,
    "AUTH_COOKIE_SAMESITE": "Strict",
}