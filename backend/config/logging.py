# config/logging.py
from pathlib import Path

LOG_DIR = Path("/app/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# COMMON_HANDLERS = ["console", "general_file"]
COMMON_HANDLERS = ["general_file"]

BASE_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "request_id": {"()": "config.logging_filters.RequestIDFilter"},
        "drop_request_obj": {"()": "config.logging_filters.DropNonSerializableFilter"},
    },
    "formatters": {
        "simple": {
            "format": "{levelname} {name} {message}",
            "style": "{",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(module)s %(message)s %(request_id)s",
            "rename_fields": {"asctime": "timestamp", "levelname": "level"},
            "json_ensure_ascii": False,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filters": ["request_id", "drop_request_obj"],
        },
        "general_file": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "json",
            "filters": ["request_id", "drop_request_obj"],
        },
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
    "root": {
        "level": "WARNING",
        "handlers": COMMON_HANDLERS,
    },
    "loggers": {
        "django": {
            "level": "INFO",
            "handlers": COMMON_HANDLERS,
            "propagate": False,
        },
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
        "apps": {
            "level": "DEBUG",
            "handlers": COMMON_HANDLERS,
            "propagate": False,
        },
        "config.exceptions": {
            "level": "WARNING",
            "handlers": COMMON_HANDLERS + ["core_errors"],
            "propagate": False,
        },
    },
}


def merge_logging_configs(*module_configs) -> dict:
    from copy import deepcopy

    result = deepcopy(BASE_LOGGING)

    for module_config in module_configs:
        for section in ("handlers", "loggers", "formatters", "filters"):
            result[section].update(module_config.get(section, {}))
        if "root" in module_config:
            result["root"].update(module_config["root"])

    return result
