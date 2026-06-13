from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOGGING = {
    "handlers": {
        "files_file": {
            "class": "logging.FileHandler",
            "filename": str(BASE_DIR / "files.log"),
            "encoding": "utf-8",
            "level": "INFO",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "apps.files": {
            "level": "DEBUG",
            "handlers": ["err", "dbg", "inf", "files_file"],
            "propagate": False,
        },
    },
}
