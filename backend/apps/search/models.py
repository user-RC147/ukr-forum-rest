from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "category"
        ordering = ["-id"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self) -> str:
        return self.name


class TagModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        to=CategoryModel, on_delete=models.CASCADE, related_name="tags"
    )

    class Meta:
        db_table = "tag"
        ordering = ["-id"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return f"{self.name} {self.category.name}"
