from pathlib import Path
import uuid

from django.db import models
from django.utils import timezone


def file_directory_path(instance, filename):
    today = timezone.now()

    ext = Path(filename).suffix

    filename = f"{uuid.uuid4()}{ext}"

    return Path(
        "files",
        str(instance.owner_id),
        str(today.year),
        f"{today.month:02}",
        f"{today.day:02}",
        filename,
    ).as_posix()


class FileModel(models.Model):
    file = models.FileField(upload_to=file_directory_path, max_length=100)
    name = models.CharField(max_length=100, blank=False)
    owner_id = models.PositiveIntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    vizible = models.BooleanField(default=True)

    class Meta:
        db_table = "file"
        ordering = ["-id"]
        verbose_name = "Файл"
        verbose_name_plural = "Файли"

    def __str__(self) -> str:

        if len(self.name) > 15:
            title = self.name[:16] + self.name.split(".")[-1]
        else:
            title = self.name

        return f"{title} - {self.created_at}"
