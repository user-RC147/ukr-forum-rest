from django.contrib import admin

from apps.files.models import FileModel

# Register your models here.


@admin.register(FileModel)
class FileAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    search_fields = ["title", "mime_type"]
