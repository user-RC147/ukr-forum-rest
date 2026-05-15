BASE_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "err": {
            "class": "logging.FileHandler",
            "filename": "general.log",
            "level": "WARNING",
            "formatter": "verbose",
        },
        "dbg": {
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "level": "DEBUG",
            "formatter": "simple",
        },
        "inf": {
            "class": "logging.StreamHandler",
            "filters": ["require_debug_false"],
            "level": "INFO",
            "formatter": "simple",
        },
    },
    "loggers": {},
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
}



#merge configs from modules
def merge_logging_configs(*module_configs) -> dict:

    from copy import deepcopy

    result = deepcopy(BASE_LOGGING)

    for module_config in module_configs:
        for section in ("handlers", "loggers", "formatters", "filters"):
            result[section].update(module_config.get(section, {}))

    return result