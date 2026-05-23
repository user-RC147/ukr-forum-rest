from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOGGING = {
    "handlers": {
        "shop_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(BASE_DIR / "shop.log"),
            "encoding": "utf-8",
            'delay': True,
            "level": "INFO",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "shop": {
            "level": "DEBUG",
            "handlers": ["err", "dbg", "inf", "shop_file"],
            "propagate": False,
        },
    },
}
