from django.db import models

class ProductModel(models.Model):
    title = models.CharField(max_length=300, blank=False)
    description = models.CharField(max_length=1500)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # owner = models.ForeignKey("users.User", on_delete=models.CASCADE, db_column="owner_id")

    class Meta:
        db_table = "product"
        ordering = ["-id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        if self.updated_at != self.created_at:
            return f"(upd: {self.updated_at:%d.%m.%Y}){self.title} - {self.price} грн."
        return f"(created: {self.created_at:%d.%m.%Y}){self.title} - {self.price} грн."
