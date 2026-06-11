from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOGGING = {
    "handlers": {
        "search_file": {
            "class": "logging.FileHandler",
            "filename": str(BASE_DIR / "search.log"),
            "encoding": "utf-8",
            "level": "INFO",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "apps.search": {
            "level": "DEBUG",
            "handlers": ["err", "dbg", "inf", "files_file"],
            "propagate": False,
        },
    },
}
