from collections.abc import Iterable, Sequence
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile

from apps.files.models import FileModel

from .contracts.exceptions import FileNotFoundError
from .dtos import FileRepoDTO
from .ports import FileRepositoryPort, UploadedFileLike

logger = logging.getLogger(__name__)


class FileRepository:
    def __init__(self, model=FileModel) -> None:
        self.model = model

    def _get_model(self, id: int, event: str = "get_file"):
        try:
            result = self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            raise FileNotFoundError(extra={"file_id": id, "event": event})

        return result

    def get(self, id: int) -> FileRepoDTO:
        result = self._get_model(id=id)

        return _to_dto(result)

    def get_many(self, ids: list[int]) -> list[FileRepoDTO]:
        files = self.model.objects.filter(id__in=ids)
        if len(files) < len(ids):
            found_ids = {f.id for f in files}
            missing = set(ids) - found_ids
            logger.warning(
                "Files not found",
                extra={"not_found_ids": missing, "event": "get_many_file"},
            )
        return [_to_dto(f) for f in files]

    def delete(self, id: int) -> tuple[str, str | None]:
        instance = self._get_model(id, event="delete_file")

        file_path = instance.file
        thumbnail_path = instance.thumbnail
        instance.delete()
        return str(file_path), str(thumbnail_path) if thumbnail_path else None

    def delete_many(self, ids: Sequence[int]) -> tuple[list[str], list[str] | None]:
        data = self.model.objects.filter(id__in=ids)
        if len(data) < len(ids):
            found_ids = {f.id for f in data}
            missing = set(ids) - found_ids
            logger.error(
                "Not all files was deleted!",
                extra={"not_found_ids": missing, "event": "delete_many_file"},
            )
        file_paths = list(data.values_list("file", flat=True))
        thumbnail_paths = list(data.values_list("thumbnail", flat=True))
        thumbnail_paths = [i for i in thumbnail_paths if i]
        data.delete()

        return file_paths, thumbnail_paths if thumbnail_paths else None

    def create_many(
        self, data: Iterable[UploadedFileLike], user_id: int
    ) -> list[FileRepoDTO]:
        instances = [self.model(name=d.name, file=d, owner_id=user_id) for d in data]

        result = self.model.objects.bulk_create(instances)

        return [_to_dto(r) for r in result]

    def create(self, data, file: UploadedFileLike, user_id: int) -> FileRepoDTO:
        result = self.model.objects.create(name=data.name, file=file, owner_id=user_id)
        return _to_dto(result)

    def filter_by_id(self, ids: Iterable[int]) -> list[FileRepoDTO]:
        result = self.model.objects.filter(id__in=ids)
        return [_to_dto(r) for r in result]

    def update_files_content(
        self, updates: dict[int, UploadedFileLike]
    ) -> tuple[list[FileRepoDTO], list[str]]:
        ids = list(updates.keys())
        files_by_id = self.model.objects.filter(id__in=ids).in_bulk()
        old_paths = [files_by_id[i].file.name for i in ids]

        updated = []
        for file_id, upload in updates.items():
            file = files_by_id[file_id]
            file.name = upload.name
            file.file.save(upload.name, ContentFile(upload.file.read()), save=False)
            updated.append(file)

        self.model.objects.bulk_update(updated, ["name", "file"])
        return [_to_dto(u) for u in updated], old_paths


def _to_dto(data: FileModel) -> FileRepoDTO:
    return FileRepoDTO(
        id=data.id,
        name=data.name,
        created_at=data.created_at,
        owner_id=data.owner_id,
        file=data.file.url,
        thumbnail=data.thumbnail.url if data.thumbnail else None,
        visible=data.visible,
    )


def get_file_repo() -> FileRepositoryPort:
    return FileRepository()
