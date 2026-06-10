from typing import Protocol

from django.core.files.uploadedfile import UploadedFile

from apps.files.dto import FileDTO


class FileProtocol(Protocol):
    def create_file(self, data: UploadedFile, user_id: int) -> FileDTO: ...

    def create_files_list(
        self, data: list[UploadedFile], user_id: int
    ) -> list[FileDTO]: ...

    def get_file(self, file_id: int) -> FileDTO:...

    def delete_file(self, file_id: int) -> None:...

    def delete_files_map(self, files_ids: list[int]) -> None:...

    def get_files_map(self, files_ids: list[int]) -> dict[int, FileDTO]: ...

    def update_files_map(self, data: list[UploadedFile], user_id: int, target_ids: list[int]
    ) -> list[FileDTO]: ...
