from pathlib import Path
import uuid

from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToPath:
    """
    Params for  upload_to (ImageField/FileField).
    """

    def __init__(self, field_name: str):
        self.field_name = field_name

    def __call__(self, instance, filename: str) -> str:
        today = timezone.now()
        ext = Path(filename).suffix
        filename = f"{uuid.uuid4()}{ext}"

        return Path(
            str(instance.owner_id),
            str(today.year),
            f"{today.month:02}",
            f"{today.day:02}",
            self.field_name,
            filename,
        ).as_posix()

    def __eq__(self, other):
        return isinstance(other, UploadToPath) and self.field_name == other.field_name


class FileModel(models.Model):
    file = models.FileField(
        upload_to=UploadToPath("file"),
        max_length=100,
        verbose_name="Шлях до файлу",  # ~800px after resizing, for details
    )

    thumbnail = models.ImageField(
        upload_to=UploadToPath("thumbnail"), null=True, blank=True
    )  # ~300px, for lists

    is_processed = models.BooleanField(default=False)

    name = models.CharField(max_length=100, blank=False, verbose_name="Ім'я файлу")
    owner_id = models.PositiveIntegerField(
        blank=False, verbose_name="Айді власника(юзера)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    visible = models.BooleanField(default=True, verbose_name="Видимість")

    class Meta:
        db_table = "file"
        ordering = ["-id"]
        verbose_name = "Файл"
        verbose_name_plural = "Файли"

    def __str__(self) -> str:
        if len(self.name) > 16:
            ext = Path(self.name).suffix
            name = f"{Path(self.name).stem[:12]}…{ext}"
        else:
            name = self.name

        return f"[{self.id}] {name} (owner: {self.owner_id})"
