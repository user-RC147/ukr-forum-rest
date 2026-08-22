from decimal import Decimal
from typing import Any
from django.db import models

from django.conf import settings

from .market import Market
from .asset import Asset


class Purchase(models.Model):
    """Чек / витрата — прив'язана до активу і магазину."""

    asset=models.ForeignKey(
        'Asset',
        on_delete=models.CASCADE,
        related_name="purchases",
    )

    market=models.ForeignKey(
        'Market',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,        
        verbose_name="Магазин",
    )

    created_by: models.ForeignKey[Any | None]=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    data_purchase=models.DateField(
        verbose_name="Дата покупки",
    )

    note = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "household_purchase"
        ordering = ["-data_purchase"]

    def __str__(self):
        return f"{self.asset.name} / {self.market} / {self.data_purchase}"

    @property
    def total_amount(self):
        return sum(
            (item.total_price for item in self.items.all()),
            Decimal('0.00')
        )
