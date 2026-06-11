from django.core.files.uploadedfile import UploadedFile

from apps.files.dto import FileDTO
from apps.files.protocols import FileProtocol
from apps.files.services import FileService


class FileContract:
    def __init__(self) -> None:
        self.service = FileService()

    def create(self, data: UploadedFile, user_id: int) -> FileDTO:
        return self.service.create(data, user_id)

    def get(self, file_id: int) -> FileDTO:
        return self.service.get(file_id)

    def get_many(self, files_ids: list[int]) -> dict[int, FileDTO]:
        return self.service.get_many(files_ids)

    def create_many(
        self, data: list[UploadedFile], user_id: int
    ) -> list[FileDTO]:
        return self.service.create_many(data, user_id)

    def delete(self, file_id: int) -> None:

        return self.service.delete(file_id)

    def delete_many(self, files_ids: list[int]) -> None:
        return self.service.delete_many(files_ids)

    def update_many(
        self, data: list[UploadedFile], user_id: int, target_ids: list[int]
    ) -> list[FileDTO]:
        return self.service.update_many(data, user_id, target_ids)


def get_file_contract() -> FileProtocol:
    return FileContract()
