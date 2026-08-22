from collections.abc import Mapping, Sequence
from typing import Protocol

from apps.files.contracts.dtos import FileDTO, FileUpdatePlan
from core.contracts.ports.files import UploadedFileLike


class FileProtocol(Protocol):
    def create(self, data: UploadedFileLike, user_id: int) -> FileDTO: ...

    def create_many(
        self, data: Sequence[UploadedFileLike], user_id: int
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
        update_files: Mapping[int, UploadedFileLike] | None = None,
        create_files: Sequence[UploadedFileLike] | None = None,
    ) -> list[FileDTO]: ...
