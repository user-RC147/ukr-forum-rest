import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import UploadedFile
from dto import FileDTO
from exceptions import FileExtensionError, FileNameError, FileSizeError

from apps.files.models import FileModel

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

    def create_file(self, data: UploadedFile, user_id: int) -> FileDTO:
        ext = data.name.split(".")[-1]
        if ext not in ALLOWED_EXTENSIONS:
            logger.info(
                "Downloaded file with non-supported extention: %s, from user_id: %s",
                ext,
                user_id,
            )
            raise FileExtensionError(
                f"Extension is not supported! Try: {ALLOWED_EXTENSIONS}"
            )
        if data.size > ALLOWED_SIZE:
            logger.info(
                "Downloaded file with too big size: %s, from user_id: %s",
                data.size,
                user_id,
            )
            raise FileSizeError(
                f"File size is too big (size: {data.size}! Try this size: {ALLOWED_SIZE})!"
            )
        if len(data.name) > ALLOWED_NAMESIZE:
            logger.info(
                "Downloaded file name too long: %s, from user_id: %s",
                len(data.name),
                user_id,
            )
            raise FileNameError(
                f"File name is too long ({len(data.name)})! Try with max name size: {ALLOWED_NAMESIZE}"
            )

        result = self.model.objects.create(
            name=data.name, file=data.file, owner_id=user_id
        )

        return FileDTO(
            owner_id=result.owner_id,
            file_id=result.id,
            file=result.file,
            vizible=result.vizible,
            created_at=result.created_at,
        )

    def get_file(self, file_id: int) -> FileDTO:
        try:
            result = self.model.objects.get(id=file_id)
        except ObjectDoesNotExist:
            logger.info("Object with id:%s not found!", file_id)

        return FileDTO(
            owner_id=result.owner_id,
            file_id=result.id,
            file=result.file,
            vizible=result.vizible,
            created_at=result.created_at,
        )

    def delete_file(self, file_id: int, user_id: int) -> None:
        # if not get_user(user_id):
        #     raise AttributeError
        self.model.objects.get(id=file_id).delete()
        logger.info("File with id:%s was deleted by user_id:%s", file_id, user_id)
