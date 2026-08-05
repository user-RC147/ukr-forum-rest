from django.db import models

from apps.geo.models.country import Country
from apps.geo.models.region import Region


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва міста")
    name_ua = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Назва українською"
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities", verbose_name="Країна"
    )
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="cities", verbose_name="Регіон"
    )
    api_id = models.PositiveIntegerField(
        null=True, blank=True, unique=True, verbose_name="ID в Geo API"
    )
    latitude = models.DecimalField(
        max_digits=20, decimal_places=16, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=20, decimal_places=16, null=True, blank=True
    )

    class Meta:
        db_table = "geo_city"
        verbose_name = "Місто"
        verbose_name_plural = "Міста"
        ordering = ["country__name", "region__name", "name"]

    def __str__(self):
        return f"{self.name}"
