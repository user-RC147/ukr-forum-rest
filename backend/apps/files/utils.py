import logging
import os

from django.conf import settings

logger = logging.getLogger(__name__)

# core - never del
_UPLOAD_ROOT = os.path.join(settings.MEDIA_ROOT, "files")


def _cleanup_empty_parent_dirs(file_path: str) -> None:
    """Del empty folders"""
    current = os.path.dirname(os.path.join(settings.MEDIA_ROOT, file_path))

    while current.startswith(_UPLOAD_ROOT) and current != _UPLOAD_ROOT:
        try:
            os.rmdir(current)  # OSError if empty or not exist
            logger.debug("Removed empty directory: %s", current)
            current = os.path.dirname(current)
        except OSError:
            break  # not empty
