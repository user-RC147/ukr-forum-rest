from django.db import models

# Create your models here.


class CategoryModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class TagModel(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        to=CategoryModel, on_delete=models.CASCADE, related_name="tags"
    )

    def __str__(self) -> str:
        return f"{self.name} {self.category.name}"
