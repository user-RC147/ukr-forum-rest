from django.core.files.uploadedfile import UploadedFile
from files.protocols import FileProtocol
from files.services import FileService

from apps.files.dto import FileDTO


class FileContract:
    def __init__(self) -> None:
        self.service = FileService()

    def create_file(self, data: UploadedFile, user_id: int) -> FileDTO:
        return self.service.create_file(data, user_id)

    def get_file(self, file_id: int) -> FileDTO:
        return self.service.get_file(file_id)

    def file_delete(self, file_id: int, user_id: int) -> bool:
        self.service.delete_file(file_id, user_id)
        return True


def get_file_contract() -> FileProtocol:
    return FileContract()
