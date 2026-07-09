from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOGGING = {
    "handlers": {
        "household_file": {
            "class": "logging.FileHandler",
            "filename": str(BASE_DIR / "household.log"),
            "encoding": "utf-8",
            "level": "INFO",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "apps.household": {
            "level": "DEBUG",
            "handlers": ["err", "dbg", "inf", "geo_file"],
            "propagate": False,
        },
    },
}
