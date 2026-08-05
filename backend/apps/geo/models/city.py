from django.contrib.postgres.indexes import GinIndex, OpClass
from django.db import models

from apps.geo.models.country import CountryModel


class CityModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва міста")
    name_ua = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Назва українською"
    )
    country = models.ForeignKey(
        CountryModel,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name="Країна",
    )
    region = models.ForeignKey(
        CountryModel,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name="Регіон",
    )
    api_id = models.PositiveIntegerField(
        null=True, blank=True, unique=True, verbose_name="ID в Geo API"
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    class Meta:
        db_table = "geo_city"
        verbose_name = "Місто"
        verbose_name_plural = "Міста"
        ordering = ["country__name", "region__name", "name"]

        indexes = [
            GinIndex(OpClass("name", name="gin_trgm_ops"), name="name_trgm_idx"),
            GinIndex(OpClass("name_ua", name="gin_trgm_ops"), name="name_ua_trgm_idx"),
        ]

    def __str__(self):
        return f"{self.name}"
