from django.contrib.postgres.indexes import GinIndex, OpClass
from django.contrib.postgres.search import SearchVector
from django.db import models

from .enums import PRODUCT_STATUS_LABELS, ProductStatus


class ProductModel(models.Model):
    title = models.CharField(max_length=300, blank=False)
    description = models.CharField(max_length=1500)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)

    status = models.CharField(
        max_length=10,
        choices=[(s.value, PRODUCT_STATUS_LABELS[s]) for s in ProductStatus],
        default=ProductStatus.NEW.value,
    )

    owner_id = models.PositiveIntegerField(blank=False)
    category_id = models.IntegerField()

    country_id = models.PositiveIntegerField(blank=False, null=True)
    region_id = models.PositiveIntegerField(null=True)
    city_id = models.PositiveIntegerField(blank=False, null=True)

    class Meta:
        db_table = "product"
        ordering = ["-id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["category_id"]),
            models.Index(fields=["country_id"]),
            models.Index(fields=["region_id"]),
            models.Index(fields=["city_id"]),
            GinIndex(
                SearchVector("title", "description", config="simple"),
                name="shop_product_search_gin",
            ),
            GinIndex(
                OpClass("description", name="gin_trgm_ops"), name="description_trgm_idx"
            ),
        ]

    def __str__(self):
        if self.updated_at != self.created_at:
            return f"(upd: {self.updated_at:%d.%m.%Y}){self.title} - {self.price} грн."
        return f"(created: {self.created_at:%d.%m.%Y}){self.title} - {self.price} грн."


class ProductFileModel(models.Model):
    file_id = models.PositiveIntegerField()

    product = models.ForeignKey(
        to=ProductModel,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Файли товара",
    )

    class Meta:
        db_table = "file_product"
        ordering = ["-id"]
        verbose_name = "Файл товару"
        verbose_name_plural = "Файли товарів"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "file_id"], name="uniq_product_file"
            )
        ]
        indexes = [
            models.Index(fields=["file_id"]),
        ]

    def __str__(self):
        return f"[{self.file_id}] for product with id: {self.product.pk}"
