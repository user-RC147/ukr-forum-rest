import os
from pathlib import Path

DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() in ("1", "true", "yes")

LOG_DIR = Path("/app/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


# BASE_DIR = Path(__file__).resolve().parent.parent
# LOG_DIR = BASE_DIR / "logs"
# LOG_DIR.mkdir(parents=True, exist_ok=True)


COMMON_HANDLERS = ["console", "json_stream"] if DEBUG else ["json_stream"]

BASE_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": "config.logging_filters.RequestIDFilter"},
        "user_id": {"()": "config.logging_filters.UserIDFilter"},
        "drop_request_obj": {"()": "config.logging_filters.DropNonSerializableFilter"},
    },
    "formatters": {
        "simple": {"format": "{levelname} {name} {message}", "style": "{"},
        "json": {
            "()": "pythonjsonlogger.json.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(module)s %(message)s %(request_id)s %(user_id)s",
            "rename_fields": {"asctime": "timestamp", "levelname": "level"},
            "json_ensure_ascii": False,
            "defaults": {"request_id": None, "user_id": None},
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filters": ["request_id", "drop_request_obj", "user_id"],
        },
        "json_stream": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "json",
            "filters": ["request_id", "drop_request_obj", "user_id"],
        },
        # backup logs, NOT FOR PROMTAIL
        "core_errors": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "core_errors.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "level": "WARNING",
            "formatter": "json",
            "filters": ["request_id", "drop_request_obj", "user_id"],
        },
    },
    "root": {"level": "WARNING", "handlers": COMMON_HANDLERS},
    "loggers": {
        "django": {"level": "INFO", "handlers": COMMON_HANDLERS, "propagate": False},
        "django.request": {
            "level": "ERROR",
            "handlers": COMMON_HANDLERS,
            "propagate": False,
        },
        "django.server": {
            "level": "WARNING",
            "handlers": COMMON_HANDLERS,
            "propagate": False,
        },
        "apps": {"level": "DEBUG", "handlers": COMMON_HANDLERS, "propagate": False},
        "config.drf_err_handler": {
            "level": "WARNING",
            "handlers": COMMON_HANDLERS + ["core_errors"],
            "propagate": False,
        },
    },
}
