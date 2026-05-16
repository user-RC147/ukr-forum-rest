from django.db import models
# from django.contrib.postgres.fields import ArrayField


class ProductModel(models.Model):
    title = models.CharField(max_length=300, blank=False)
    description = models.CharField(max_length=1500)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vizible = models.BooleanField(default=True)

    owner_id = models.PositiveIntegerField(blank=False)
    # category_id = ArrayField(base_field=models.IntegerField())

    class Meta:
        db_table = "product"
        ordering = ["-id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        if self.updated_at != self.created_at:
            return f"(upd: {self.updated_at:%d.%m.%Y}){self.title} - {self.price} грн."
        return f"(created: {self.created_at:%d.%m.%Y}){self.title} - {self.price} грн."
