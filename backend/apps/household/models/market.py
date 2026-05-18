from django.db import models
from django.conf import settings

from core.mixins.LocationMixin import LocationMixin


class Market(LocationMixin, models.Model):
    name=models.CharField(
        max_length=150,
        verbose_name="Магазин",
    )

    address_line=models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Адреса(вул.+дім)"
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table='household_market'
        verbose_name="Магазин"
        verbose_name_plural="Магазини"
        ordering=['name']

    def __str__(self):
        return f"{self.name}"