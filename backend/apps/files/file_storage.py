import logging
import os
from typing import Protocol

from django.conf import settings
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)

# core - never del
_UPLOAD_ROOT = settings.MEDIA_ROOT


class Storage(Protocol):
    def delete(self, paths: list[str] | str) -> None: ...


class DjangoStorage(Storage):
    def __init__(self, storage=default_storage) -> None:
        self.storage = storage

    def delete(self, data: list[str] | str) -> None:
        """Take path (or path list) in arguments"""
        if isinstance(data, list):
            for path in data:
                default_storage.delete(path)
                _cleanup_empty_parent_dirs(str(path))
        else:
            default_storage.delete(data)
            _cleanup_empty_parent_dirs(str(data))


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


def get_storage() -> Storage:
    return DjangoStorage()
