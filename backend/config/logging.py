import os
from pathlib import Path

DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() in ("1", "true", "yes")

LOG_DIR = Path("/app/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# В деве: и читаемый console, и json (чтобы Grafana работала локально тоже)
# В проде: только json (чище объём логов)
COMMON_HANDLERS = ["console", "json_stream"] if DEBUG else ["json_stream"]

BASE_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": "config.logging_filters.RequestIDFilter"},
        "drop_request_obj": {"()": "config.logging_filters.DropNonSerializableFilter"},
    },
    "formatters": {
        "simple": {"format": "{levelname} {name} {message}", "style": "{"},
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(module)s %(message)s %(request_id)s",
            "rename_fields": {"asctime": "timestamp", "levelname": "level"},
            "json_ensure_ascii": False,
            "defaults": {"request_id": None},
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filters": ["request_id", "drop_request_obj"],
        },
        "json_stream": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "json",
            "filters": ["request_id", "drop_request_obj"],
        },
        #backup logs, NOT FOR PROMTAIL
        "core_errors": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "core_errors.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "level": "WARNING",
            "formatter": "json",
            "filters": ["request_id", "drop_request_obj"],
        },
    },
    "root": {"level": "WARNING", "handlers": COMMON_HANDLERS},
    "loggers": {
        "django": {"level": "INFO", "handlers": COMMON_HANDLERS, "propagate": False},
        "django.request": {"level": "ERROR", "handlers": COMMON_HANDLERS, "propagate": False},
        "django.server": {"level": "WARNING", "handlers": COMMON_HANDLERS, "propagate": False},
        "apps": {"level": "DEBUG", "handlers": COMMON_HANDLERS, "propagate": False},
        "config.exceptions": {"level": "WARNING", "handlers": COMMON_HANDLERS + ["core_errors"], "propagate": False},
    },
}