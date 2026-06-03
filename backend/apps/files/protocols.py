from typing import Protocol

from django.core.files.uploadedfile import UploadedFile

from apps.files.dto import FileDTO


class FileProtocol(Protocol):
    def create_file(self, data: UploadedFile, user_id: int) -> FileDTO: ...
