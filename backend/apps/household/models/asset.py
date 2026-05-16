from django.db import models

from core.mixins.LocationMixin import LocationMixin, PrivateLocationMixin

from apps.household.models.group import Group
from apps.household.models.place_type import PlaceType


class Asset(LocationMixin,models.Model):
    """
    Конкретний актив групи — дім, авто, дача тощо.
    Локація зберігається як id (без FK до geo моделей).
    """
    name=models.CharField(
        max_length=100,
        verbose_name="Назва активу",
    )
    place_type=models.ForeignKey(
        PlaceType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assets",
        verbose_name="Тип місця",
    )
    group=models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="assets",
        verbose_name="Група",
    )
    country_id = models.IntegerField(
        null=True, blank=True, verbose_name="ID країни"
    )
    region_id = models.IntegerField(
        null=True, blank=True, verbose_name="ID регіону"
    )
    city_id = models.IntegerField(
        null=True, blank=True, verbose_name="ID міста"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Адреса (вулиця, дім)",
    )

    class Meta:
        db_table = "household_asset"
        verbose_name = "Актив"
        verbose_name_plural = "Активи"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.group.name})"