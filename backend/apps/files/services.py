from collections.abc import Mapping, Sequence
import logging

from django.conf import settings

from apps.files.contracts.dtos import FileDTO, FileUpdatePlan
from apps.files.contracts.exceptions import (
    AppValidationError,
    FileExtensionError,
    FileNameError,
    FileSizeError,
)
from apps.files.dtos import FileRepoDTO
from apps.files.file_storage import Storage, get_storage
from core.unit_of_work.uow import get_unit_of_work
from core.unit_of_work.uow_protocol import UnitOfWork

from .ports import FileRepositoryPort, UploadedFileLike
from .repository import get_file_repo
from .tasks import delete_files_task, process_file_task

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {
    "jpg",
    "png",
    "svg",
}

ALLOWED_SIZE = 10 * 1024 * 1024

ALLOWED_NAMESIZE = 300


class FileService:
    def __init__(
        self, repo: FileRepositoryPort, storage: Storage, uow: UnitOfWork
    ) -> None:
        self.repo = repo
        self.storage = storage
        self.uow = uow

    def create(self, data: UploadedFileLike, user_id: int) -> FileDTO:
        self._validate_file(data)

        result = self.repo.create(data.name, data, user_id)
        logger.info(
            "File created", extra={"file_id": result.id, "event": "create_file"}
        )
        return _to_dto(result)

    def get(self, file_id: int) -> FileDTO:

        result = self.repo.get(id=file_id)

        return _to_dto(result)

    def get_many(self, file_ids: list[int]) -> dict[int, FileDTO]:
        if not file_ids:
            return {}

        files = self.repo.get_many(file_ids)

        return {f.id: _to_dto(f) for f in files}

    def delete(self, file_id: int) -> None:
        with self.uow:
            file_path, thumbnail_path = self.repo.delete(file_id)

            self.uow.on_commit(lambda: delete_files_task.delay(file_path))
            if thumbnail_path:
                self.uow.on_commit(lambda: delete_files_task.delay(thumbnail_path))

        logger.info(
            "File was deleted", extra={"file_id": file_id, "event": "delete_file"}
        )

    def delete_many(self, file_ids: list[int]) -> None:
        if not file_ids:
            return

        with self.uow:
            file_paths, thumbnail_paths = self.repo.delete_many(file_ids)

            self.uow.on_commit(lambda: delete_files_task.delay(file_paths))
            if thumbnail_paths:
                self.uow.on_commit(lambda: delete_files_task.delay(thumbnail_paths))

        logger.info(
            "Files was deleted",
            extra={
                "file_ids": file_ids,
                "amount": len(file_paths),
                "event": "delete_many_file",
            },
        )

    def create_many(
        self, data: Sequence[UploadedFileLike], user_id: int
    ) -> list[FileDTO]:

        if not data:
            return []

        for d in data:
            self._validate_file(d)

        with self.uow:
            result = self.repo.create_many(data, user_id)

        for r in result:
            process_file_task.delay(r.id)
        dto = [_to_dto(r) for r in result]

        logger.info(
            "Files was created",
            extra={"file_ids": [d.id for d in dto], "event": "create_many_file"},
        )

        return dto

    def update_many(
        self,
        user_id: int,
        item_ids: list[int],
        plan: FileUpdatePlan | None = None,
        update_files: Mapping[int, UploadedFileLike] | None = None,
        create_files: Sequence[UploadedFileLike] | None = None,
    ) -> list[FileDTO]:
        plan = plan or FileUpdatePlan()
        update_files = update_files or {}
        create_files = create_files or []

        self._validate_ids(item_ids, plan)
        self._validate_update_mapping(plan, update_files)
        for f in (*update_files.values(), *create_files):
            self._validate_file(f)

        new_file_paths: list[str] = []
        try:
            with self.uow:
                result: list[FileDTO] = []

                updated, old_paths = self._apply_updates(plan, update_files)
                new_file_paths.extend(f.file for f in updated)
                result.extend(_to_dto(f) for f in updated)
                if old_paths:
                    self.uow.on_commit(
                        lambda paths=old_paths: self.storage.delete(paths)
                    )

                created = self._apply_creates(user_id, create_files)
                result.extend(created)

                result.extend(self._apply_keep(plan))

                self._apply_deletes(item_ids, plan)
        except Exception:
            self.storage.delete(new_file_paths)
            logger.error(
                "Unexpected error when try update many files. New files was deleted.",
                extra={
                    "item_file_ids": item_ids,
                    "update_file_ids": plan.update_ids,
                    "create_file_amount": len(create_files),
                    "update_file_amount": len(update_files),
                    "keep_file_ids": plan.keep_ids,
                    "event": "file_validation",
                },
            )
            raise
        return result

    def _validate_ids(self, item_ids: list[int], plan: FileUpdatePlan) -> None:
        check = set(item_ids) | plan.touched_ids()
        existing_ids = {i.id for i in self.repo.filter_by_id(check)}
        invalid_ids = check - existing_ids
        if invalid_ids:
            raise AppValidationError(
                "File ids invalid!",
                extra={
                    "invalid_ids": list(invalid_ids),
                    "event": "file_validation",
                },
            )

    def _validate_update_mapping(
        self, plan: FileUpdatePlan, update_files: dict[int, UploadedFileLike]
    ) -> None:
        expected = set(plan.update_ids)
        got = set(update_files.keys())
        if expected != got:
            raise AppValidationError(
                f"update_files keys must match update_ids exactly: expected {expected}, got {got}",
                extra={
                    "expected": list(expected),
                    "got": list(got),
                    "event": "file_validation",
                },
            )

    def _apply_updates(
        self, plan: FileUpdatePlan, update_files: dict[int, UploadedFileLike]
    ) -> tuple[list[FileRepoDTO], list[str]]:
        if not plan.update_ids:
            return [], []

        updated, old_paths = self.repo.update_files_content(update_files)

        logger.info(
            "Updated files",
            extra={"update_ids": plan.update_ids, "event": "update_files"},
        )
        return updated, old_paths

    def _apply_creates(
        self, user_id: int, create_files: list[UploadedFileLike]
    ) -> list[FileDTO]:
        if not create_files:
            return []
        created = self.create_many(create_files, user_id)
        logger.info(
            "Created files",
            extra={"create_ids": [i.id for i in created], "event": "update_files"},
        )
        return created

    def _apply_keep(self, plan: FileUpdatePlan) -> list[FileDTO]:
        if not plan.keep_ids:
            return []
        return [_to_dto(f) for f in self.repo.filter_by_id(plan.keep_ids)]

    def _apply_deletes(self, item_ids: list[int], plan: FileUpdatePlan) -> None:
        delete_ids = set(item_ids) - plan.touched_ids()
        if not delete_ids:
            return
        delete_ids = list(delete_ids)
        self.delete_many(delete_ids)
        logger.info(
            "Deleted files",
            extra={"delete_ids": delete_ids, "event": "update_files"},
        )

    @staticmethod
    def _validate_file(data: UploadedFileLike) -> None:
        if "." not in data.name:
            raise FileExtensionError(
                "File has no extension", extra={"event": "file_validation"}
            )

        ext = data.name.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise FileExtensionError(
                f"Extension is not supported! Try: {ALLOWED_EXTENSIONS}",
                extra={"file_ext": ext, "event": "file_validation"},
            )

        if data.size > ALLOWED_SIZE:
            raise FileSizeError(
                f"File size is too big! Try with size: {ALLOWED_SIZE} MB!",
                extra={
                    "file_size": data.size,
                    "event": "file_validation",
                },
            )

        if len(data.name) > ALLOWED_NAMESIZE:
            raise FileNameError(
                f"File name is too long! Try with name size: {ALLOWED_NAMESIZE} symbols",
                extra={
                    "file_name_size": len(data.name),
                    "event": "file_validation",
                },
            )


def _to_dto(file: FileRepoDTO) -> FileDTO:
    return FileDTO(
        owner_id=file.owner_id,
        id=file.id,
        file=f"{settings.BASE_URL}{file.file}",
        thumbnail=f"{settings.BASE_URL}{file.thumbnail}" if file.thumbnail else None,
        visible=file.visible,
    )


def get_file_service() -> FileService:
    return FileService(
        repo=get_file_repo(), storage=get_storage(), uow=get_unit_of_work()
    )
