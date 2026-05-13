from django.db import models
from apps.geo.models.country import Country

class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва регіону")
    name_ua = models.CharField(max_length=100, blank=True, default="", verbose_name="Назва українською")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions", verbose_name="Країна")
    api_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="ID в Geo API")

    class Meta:
        db_table = "geo_region"
        verbose_name = "Регіон"
        verbose_name_plural = "Регіони"
        unique_together = ("name", "country")
        ordering = ["country__name", "name"]

    def __str__(self):
        return f"{self.name}"