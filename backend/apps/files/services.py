import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from apps.files.dto import FileDTO, FileUpdatePlan
from apps.files.exceptions import FileExtensionError, FileNameError, FileSizeError, AppValidationError, FileNotFoundError
from apps.files.models import FileModel
from apps.files.utils import _cleanup_empty_parent_dirs

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {
    "jpg",
    "png",
    "svg",
}

ALLOWED_SIZE = 10 * 1024 * 1024

ALLOWED_NAMESIZE = 300


class FileService:
    def __init__(self, model=FileModel) -> None:
        self.model = model

    def create(self, data: UploadedFile, user_id: int) -> FileDTO:
        self._validate_file(data, user_id)

        result = self.model.objects.create(name=data.name, file=data, owner_id=user_id)
        logger.info("File created", extra={"file_id": result.id, "event": "create_file"})
        return _to_dto(result)

    def get(self, file_id: int) -> FileDTO:
        try:
            result = self.model.objects.get(id=file_id)
        except ObjectDoesNotExist:
            raise FileNotFoundError(extra={"file_id": file_id, "event": "get_file"})

        return _to_dto(result)

    def get_many(self, file_ids: list[int]) -> dict[int, FileDTO]:
        if not file_ids:
            return {}

        files = self.model.objects.filter(id__in=file_ids)

        found_ids = {f.id for f in files}
        missing = set(file_ids) - found_ids
        if missing:
            logger.warning("Files not found", extra={"not_found_ids": missing, "event": "get_many_file"})

        return {f.id: _to_dto(f) for f in files}

    def delete(self, file_id: int) -> None:
        with transaction.atomic():
            try:
                instance = self.model.objects.get(id=file_id)
                file_path = instance.file
                instance.delete()
            except ObjectDoesNotExist:
                raise FileNotFoundError(extra={"file_id": file_id, "event": "delete_file"})

            transaction.on_commit(lambda: _cleanup_disk(file_path))

        logger.info("File was deleted", extra={"file_id": file_id, "event": "delete_file"})

    def delete_many(self, file_ids: list[int]) -> None:
        if not file_ids:
            return
        data = self.model.objects.filter(id__in=file_ids)
        file_paths = list(data.values_list("file", flat=True))

        with transaction.atomic():
            deleted_count, _ = data.delete()

            transaction.on_commit(lambda: _cleanup_disk(file_paths))

        logger.info(
            "Files was deleted",
            extra={
                "file_ids": file_ids,
                "amount": deleted_count,
                "event": "delete_many_file",
            },
        )

    def create_many(self, data: list[UploadedFile], user_id: int) -> list[FileDTO]:

        if not data:
            return []

        for d in data:
            self._validate_file(d, user_id)

        instances = [
        self.model(name=d.name, file=d, owner_id=user_id)
        for d in data
        ]

        with transaction.atomic():
            result = self.model.objects.bulk_create(instances)
        dto = [_to_dto(r) for r in result]

        logger.info("Files was created", extra={"file_ids": [d.id for d in dto], "event": "create_many_file"})

        return dto

    def update_many(
        self,
        user_id: int,
        item_ids: list[int],
        plan: FileUpdatePlan | None = None,
        update_files: dict[int, UploadedFile] | None = None,
        create_files: list[UploadedFile] | None = None,
    ) -> list[FileDTO]:
        plan = plan or FileUpdatePlan()
        update_files = update_files or {}
        create_files = create_files or []

        self._validate_ids(user_id, item_ids, plan)
        self._validate_update_mapping(user_id, plan, update_files)
        for f in (*update_files.values(), *create_files):
            self._validate_file(f, user_id)

        new_file_paths: list[str] = []
        try:
            with transaction.atomic():
                result: list[FileDTO] = []

                updated, old_paths = self._apply_updates(user_id, plan, update_files)
                new_file_paths.extend(f.file.name for f in updated)
                result.extend(_to_dto(f) for f in updated)
                if old_paths:
                    transaction.on_commit(lambda paths=old_paths: _cleanup_disk(paths))

                created = self._apply_creates(user_id, create_files)
                result.extend(created)

                result.extend(self._apply_keep(plan))

                self._apply_deletes(user_id, item_ids, plan)
        except Exception:
            _cleanup_disk(new_file_paths)
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

    def _validate_ids(self, user_id: int, item_ids: list[int], plan: FileUpdatePlan) -> None:
        check = set(item_ids) | plan.touched_ids()
        existing_ids = set(
            self.model.objects.filter(id__in=check).values_list("id", flat=True)
        )
        invalid_ids = check - existing_ids
        if invalid_ids:
            raise AppValidationError(
                "File ids invalid!",
                extra={
                    "invalid_ids": list(invalid_ids),
                    "event": "file_validation",
                },
            )

    def _validate_update_mapping(self, user_id: int, plan: FileUpdatePlan, update_files: dict[int, UploadedFile]) -> None:
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
        self, user_id: int, plan: FileUpdatePlan, update_files: dict[int, UploadedFile]
    ) -> tuple[list, list[str]]:
        if not plan.update_ids:
            return [], []

        files_by_id = self.model.objects.filter(id__in=plan.update_ids).in_bulk()
        old_paths = [files_by_id[i].file.name for i in plan.update_ids]

        updated = []
        for file_id in plan.update_ids:
            file = files_by_id[file_id]
            upload = update_files[file_id]
            file.name = upload.name
            file.file.save(upload.name, ContentFile(upload.file.read()), save=False)
            updated.append(file)

        self.model.objects.bulk_update(updated, fields=["name", "file"])
        logger.info(
            "Updated files",
            extra={"update_ids": plan.update_ids, "event": "update_files"},
        )
        return updated, old_paths


    def _apply_creates(self, user_id: int, create_files: list[UploadedFile]) -> list[FileDTO]:
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
        return [_to_dto(f) for f in self.model.objects.filter(id__in=plan.keep_ids)]


    def _apply_deletes(self, user_id: int, item_ids: list[int], plan: FileUpdatePlan) -> None:
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
    def _validate_file(data: UploadedFile, user_id: int) -> None:
        if "." not in data.name:
            raise FileExtensionError("File has no extension", extra={"event": "file_validation"})

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


def _to_dto(file: FileModel) -> FileDTO:
    return FileDTO(
        owner_id=file.owner_id,
        id=file.id,
        file=f"{settings.BASE_URL}{file.file.url}",
        visible=file.visible,
    )


def _cleanup_disk(data: list[str] | str):
    if isinstance(data, list):
        for path in data:
            default_storage.delete(path)
            _cleanup_empty_parent_dirs(str(path))
    else:
        default_storage.delete(data)
        _cleanup_empty_parent_dirs(str(data))