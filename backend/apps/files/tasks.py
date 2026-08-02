from celery import shared_task

from .file_storage import get_storage


@shared_task
def delete_files_task(data: list[str] | str) -> None:
    storage = get_storage()
    storage.delete(data)
