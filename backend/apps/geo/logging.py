from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOGGING = {
    "handlers": {
        "geo_file": {
            "class": "logging.FileHandler",
            "filename": str(BASE_DIR / "geo.log"),
            "encoding": "utf-8",
            "level": "INFO",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "apps.geo": {
            "level": "DEBUG",
            "handlers": ["err", "dbg", "inf", "geo_file"],
            "propagate": False,
        },
    },
}
