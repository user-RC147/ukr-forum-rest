import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from apps.files.dto import FileDTO, FileUpdatePlan
from apps.files.exceptions import FileExtensionError, FileNameError, FileSizeError, ValidationError
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

        return _to_dto(result)

    def get(self, file_id: int) -> FileDTO:
        try:
            result = self.model.objects.get(id=file_id)
        except ObjectDoesNotExist:
            logger.info("Object with id:%s not found!", file_id)
            raise FileNotFoundError

        return _to_dto(result)

    def get_many(self, file_ids: list[int]) -> dict[int, FileDTO]:
        if not file_ids:
            return {}

        files = self.model.objects.filter(id__in=file_ids)

        found_ids = {f.id for f in files}
        missing = set(file_ids) - found_ids
        if missing:
            logger.warning("Files not found for ids: %s", missing)

        return {f.id: _to_dto(f) for f in files}

    def delete(self, file_id: int) -> None:
        with transaction.atomic():
            try:
                instance = self.model.objects.get(id=file_id)
                file_path = instance.file
                instance.delete()
            except ObjectDoesNotExist:
                logger.warning("Tried to delete non-existent file id:%s", file_id)
                raise FileNotFoundError

            transaction.on_commit(lambda: _cleanup_disk(file_path))

        logger.debug("File with id:%s was deleted", file_id)

    def delete_many(self, file_ids: list[int]) -> None:
        if not file_ids:
            return
        data = self.model.objects.filter(id__in=file_ids)
        file_paths = list(data.values_list("file", flat=True))

        with transaction.atomic():
            deleted_count, _ = data.delete()

            transaction.on_commit(lambda: _cleanup_disk(file_paths))
            
        logger.debug("Deleted %d files with ids: %s", deleted_count, file_ids)

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
            return [_to_dto(r) for r in result]

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
            raise
        return result
    
    def _validate_ids(self, user_id: int, item_ids: list[int], plan: FileUpdatePlan) -> None:
        check = set(item_ids) | plan.touched_ids()
        existing_ids = set(
            self.model.objects.filter(id__in=check).values_list("id", flat=True)
        )
        invalid_ids = check - existing_ids
        if invalid_ids:
            logger.error(
                "Some ids not match with existing ids in db",
                extra={"user_id": user_id, "invalid_ids": list(invalid_ids), "event": "file_validation"},
            )
            raise ValidationError("File ids invalid!")


    def _validate_update_mapping(self, user_id: int, plan: FileUpdatePlan, update_files: dict[int, UploadedFile]) -> None:
        expected = set(plan.update_ids)
        got = set(update_files.keys())
        if expected != got:
            logger.error(
                "update_files keys not match update_ids exactly",
                extra={"user_id": user_id, "expected": list(expected), "got": list(got), "event": "file_validation"},
            )
            raise ValidationError(
                f"update_files keys must match update_ids exactly: expected {expected}, got {got}"
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
            extra={"user_id": user_id, "update_ids": plan.update_ids, "event": "update_files"},
        )
        return updated, old_paths


    def _apply_creates(self, user_id: int, create_files: list[UploadedFile]) -> list[FileDTO]:
        if not create_files:
            return []
        created = self.create_many(create_files, user_id)
        logger.info(
            "Created files",
            extra={"user_id": user_id, "create_ids": [i.id for i in created], "event": "update_files"},
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
            extra={"user_id": user_id, "delete_ids": delete_ids, "event": "update_files"},
        )

    @staticmethod
    def _validate_file(data: UploadedFile, user_id: int) -> None:
        if "." not in data.name:
            raise FileExtensionError("File has no extension.")

        ext = data.name.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            logger.info(
                "Upload rejected - unsupported extension: %s, from user_id: %s",
                ext,
                user_id,
            )
            raise FileExtensionError(
                f"Extension is not supported! Try: {ALLOWED_EXTENSIONS}"
            )
        if data.size > ALLOWED_SIZE:
            logger.info(
                "Upload rejected - large file weight: %s, from user_id: %s",
                data.size,
                user_id,
            )
            raise FileSizeError(
                f"File size is too big (size: {data.size}! Try this size: {ALLOWED_SIZE})!"
            )
        if len(data.name) > ALLOWED_NAMESIZE:
            logger.info(
                "Upload rejected - long name: %s, from user_id: %s",
                len(data.name),
                user_id,
            )
            raise FileNameError(
                f"File name is too long ({len(data.name)})! Try with max name size: {ALLOWED_NAMESIZE}"
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