import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from apps.files.dto import FileDTO
from apps.files.exceptions import FileExtensionError, FileNameError, FileSizeError
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
        try:
            instance = self.model.objects.get(id=file_id)
            file_path = instance.file
            instance.delete()
        except ObjectDoesNotExist:
            logger.warning("Tried to delete non-existent file id:%s", file_id)
            raise

        def cleanup():
            default_storage.delete(file_path)
            _cleanup_empty_parent_dirs(file_path)

        transaction.on_commit(cleanup)
        logger.debug("File with id:%s was deleted", file_id)

    def delete_many(self, file_ids: list[int]) -> None:
        if not file_ids:
            return
        data = self.model.objects.filter(id__in=file_ids)
        file_paths = list(data.values_list("file", flat=True))

        deleted_count, _ = data.delete()

        def cleanup_disk():
            for path in file_paths:
                default_storage.delete(path)
                _cleanup_empty_parent_dirs(str(path))

        transaction.on_commit(cleanup_disk)
        logger.debug("Deleted %d files with ids: %s", deleted_count, file_ids)

    def create_many(self, data: list[UploadedFile], user_id: int) -> list[FileDTO]:

        for d in data:
            self._validate_file(d, user_id)

        with transaction.atomic():
            return [self.create(f, user_id) for f in data]

    def update_many(
        self, data: list[UploadedFile], user_id: int, target_ids: list[int]
    ) -> list[FileDTO]:
        for d in data:
            self._validate_file(d, user_id)

        files = list(self.model.objects.filter(id__in=target_ids).order_by("id"))

        if not files:
            return []

        old_file_paths = [f.file.name for f in files]
        new_file_paths = []

        for file, d in zip(files, data, strict=False):
            file.name = d.name
            file.file.save(d.name, ContentFile(d.file.read()), save=False)
            new_file_paths.append(file.file.name)

        try:
            with transaction.atomic():
                self.model.objects.bulk_update(files, fields=["name", "file"])

                result = [_to_dto(f) for f in files[: len(data)]]

                if len(files) < len(data):
                    remainder = self.create_many(data[len(files) :], user_id)
                    result.extend(remainder)
                    logger.debug(
                        "Updated files with ids: %s, added files with ids: %s",
                        target_ids,
                        [i.id for i in remainder],
                    )
                elif len(files) > len(data):
                    excess = files[len(data) :]
                    delete_ids = [f.id for f in excess]
                    result = result[: len(data)]
                    self.delete_many(delete_ids)
                    logger.debug(
                        "Updated files with ids: %s, deleted files with ids: %s",
                        target_ids,
                        delete_ids,
                    )
                else:
                    logger.debug("Updated files with ids: %s", target_ids)

                def cleanup_disk():
                    for path in old_file_paths:
                        default_storage.delete(path)
                        _cleanup_empty_parent_dirs(str(path))

                transaction.on_commit(cleanup_disk)

        except Exception:
            for path in new_file_paths:
                default_storage.delete(path)
                _cleanup_empty_parent_dirs(str(path))
            raise

        return result

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
    time = file.created_at.strftime("%d.%m.%Y %H:%M:%S")
    return FileDTO(
        owner_id=file.owner_id,
        id=file.id,
        file=f"{settings.BASE_URL}/{file.file}",
        visible=file.visible,
        created_at=time,
    )
