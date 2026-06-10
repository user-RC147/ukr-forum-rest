from django.core.files.uploadedfile import UploadedFile

from apps.files.dto import FileDTO
from apps.files.protocols import FileProtocol
from apps.files.services import FileService


class FileContract:
    def __init__(self) -> None:
        self.service = FileService()

    def create_file(self, data: UploadedFile, user_id: int) -> FileDTO:
        return self.service.create_file(data, user_id)

    def get_file(self, file_id: int) -> FileDTO:
        return self.service.get_file(file_id)

    def get_files_map(self, files_ids: list[int]) -> dict[int, FileDTO]:
        return self.service.get_files_map(files_ids)

    def create_files_list(
        self, data: list[UploadedFile], user_id: int
    ) -> list[FileDTO]:
        return self.service.create_files_list(data, user_id)

    def delete_file(self, file_id: int) -> None:

        return self.service.delete_file(file_id)

    def delete_files_map(self, files_ids: list[int]) -> None:
        return self.service.delete_files_map(files_ids)

    def update_files_map(
        self, data: list[UploadedFile], user_id: int, target_ids: list[int]
    ) -> list[FileDTO]:
        return self.service.update_files_map(data, user_id, target_ids)


def get_file_contract() -> FileProtocol:
    return FileContract()
