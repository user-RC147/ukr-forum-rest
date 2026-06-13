from .base import *

# Локально DEBUG завжди True
DEBUG = True

# Додаємо debug toolbar тільки локально
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# debug toolbar показується тільки для цих IP
INTERNAL_IPS = ["127.0.0.1"]

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
