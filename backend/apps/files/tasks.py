from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image

from .enums import EXT_TO_TYPE, FileExtentions
from .file_storage import get_storage
from .models import FileModel
from .repository import FileRepository
from .utils import resize_and_encode

logger = get_task_logger(__name__)


@shared_task
def delete_files_task(data: list[str] | str) -> None:
    storage = get_storage()
    storage.delete(data)


IMAGE_SIZES = {"thumbnail": (300, 300), "file": (800, 800)}


def _process_image(pf: FileModel) -> None:
    old_path = str(pf.file)
    with default_storage.open(pf.file.name) as f:
        original = Image.open(f)
        original.load()

        for field_name, box in IMAGE_SIZES.items():
            raw_bytes = resize_and_encode(original.copy(), box)
            content = ContentFile(raw_bytes)
            filename = f"{pf.id}_{field_name}.webp"
            getattr(pf, field_name).save(filename, content, save=False)

    pf.is_processed = True
    pf.save(update_fields=["thumbnail", "file", "is_processed"])
    delete_files_task.delay(old_path)


def _process_generic(pf: FileModel) -> None:
    """
    Use if file format (type) doesn`t have any proseccors
    """
    pf.is_processed = True
    pf.save(update_fields=["is_processed"])


# Register for PROCESSORS. New type = new func + enum + register here
PROCESSORS = {
    FileExtentions.IMAGE: _process_image,
}


@shared_task(bind=True, max_retries=3, default_retry_delay=10, autoretry_for=(IOError,))
def process_file_task(self, product_file_id: int):

    pf = FileRepository()._get_model(product_file_id, "get_file_resize")

    ext = pf.name.split(".")[-1].lower()

    ext = EXT_TO_TYPE[ext]

    processor = PROCESSORS.get(ext, _process_generic)

    try:
        processor(pf)
    except Exception:
        logger.exception("Failed processing ProductFile id=%s kind=%s", pf.id, ext)
        raise
