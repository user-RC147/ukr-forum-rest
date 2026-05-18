from django.db import models

from core.mixins.LocationMixin import LocationMixin, PrivateLocationMixin

from apps.household.models.group import Group


class Asset(LocationMixin,models.Model):
    """
    Конкретний актив групи — дім, авто, дача тощо.
    Локація зберігається як id (без FK до geo моделей).
    """
    name=models.CharField(
        max_length=100,
        verbose_name="Назва активу",
    )
    group=models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="assets",
        verbose_name="Група",
    )
    address_line=models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Адреса(вул.+дім)"
    )
   

    class Meta:
        db_table = "household_asset"
        verbose_name = "Актив"
        verbose_name_plural = "Активи"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.group.name})"