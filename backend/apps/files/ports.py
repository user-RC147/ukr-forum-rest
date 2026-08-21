from collections.abc import Iterable, Mapping
from typing import Protocol

from core.contracts.ports.files import UploadedFileLike

from .dtos import FileRepoDTO


class FileRepositoryPort(Protocol):
    def get(self, id: int) -> FileRepoDTO: ...

    def get_many(self, ids: list[int]) -> list[FileRepoDTO]: ...

    def delete(self, id: int) -> tuple[str, str | None]: ...

    def delete_many(self, ids: list[int]) -> tuple[list[str], list[str] | None]: ...

    def create_many(
        self, data: Iterable[UploadedFileLike], user_id: int
    ) -> list[FileRepoDTO]: ...

    def create(self, data, file: UploadedFileLike, user_id: int) -> FileRepoDTO: ...

    def filter_by_id(self, ids: Iterable[int]) -> list[FileRepoDTO]: ...

    def update_files_content(
        self, updates: Mapping[int, UploadedFileLike]
    ) -> tuple[list[FileRepoDTO], list[str]]: ...
