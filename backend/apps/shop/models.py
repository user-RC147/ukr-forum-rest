from django.contrib.postgres.fields import ArrayField
from django.db import models


class ProductModel(models.Model):
    title = models.CharField(max_length=300, blank=False)
    description = models.CharField(max_length=1500)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)

    owner_id = models.PositiveIntegerField(blank=False)
    category_id = models.IntegerField()
    file_ids = ArrayField(base_field=models.PositiveIntegerField())

    country_id = models.PositiveIntegerField(blank=False, null=True)
    region_id = models.PositiveIntegerField(null=True)
    city_id = models.PositiveIntegerField(blank=False, null=True)

    class Meta:
        db_table = "product"
        ordering = ["-id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        if self.updated_at != self.created_at:
            return f"(upd: {self.updated_at:%d.%m.%Y}){self.title} - {self.price} грн."
        return f"(created: {self.created_at:%d.%m.%Y}){self.title} - {self.price} грн."
