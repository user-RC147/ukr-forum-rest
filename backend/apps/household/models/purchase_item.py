from django.db import models



class PurchaseItem(models.Model):
    """Рядок чеку — конкретний товар з кількістю і ціною."""

    purchase = models.ForeignKey(
        "Purchase",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    product_name_snapshot = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Назва товару",
        help_text="Зберігається автоматично при збереженні рядка чеку",
    )

    # Кількість на складі
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0,
        verbose_name="Кількість",
        help_text="Доступна кількість",
    )

    # Ціни
    price_per_unit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Ціна за одиницю",
        help_text="Ціна за 1 шт/кг/л",
    )

    # price = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="Загальна ціна",help_text="Ціна за всю наявну кількість (автоматично?)", null=True,blank=True)
    
    class Meta:
        db_table = "household_purchase_item"

    @property
    def total_price(self):
        return self.price_per_unit * self.quantity

    

    def save(self, *args, **kwargs):
        if self.product:
            self.product_name_snapshot = self.product.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name_snapshot or str(self.product)