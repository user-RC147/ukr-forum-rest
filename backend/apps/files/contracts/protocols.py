from collections.abc import Mapping, Sequence
from typing import Protocol

from django.core.files.uploadedfile import UploadedFile

from apps.files.contracts.dtos import FileDTO, FileUpdatePlan


class FileProtocol(Protocol):
    def create(self, data: UploadedFile, user_id: int) -> FileDTO: ...

    def create_many(
        self, data: Sequence[UploadedFile], user_id: int
    ) -> list[FileDTO]: ...

    def get(self, file_id: int) -> FileDTO: ...

    def delete(self, file_id: int) -> None: ...

    def delete_many(self, files_ids: list[int]) -> None: ...

    def get_many(self, files_ids: list[int]) -> dict[int, FileDTO]: ...

    def update_many(
        self,
        user_id: int,
        item_ids: list[int],
        plan: FileUpdatePlan | None = None,
        update_files: Mapping[int, UploadedFile] | None = None,
        create_files: Sequence[UploadedFile] | None = None,
    ) -> list[FileDTO]: ...
