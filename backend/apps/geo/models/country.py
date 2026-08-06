from django.contrib.postgres.indexes import GinIndex, OpClass
from django.db import models


class CountryModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва країни")
    name_ua = models.CharField(
        max_length=100, blank=True, default="", verbose_name="Назва українською"
    )
    code = models.CharField(max_length=5, unique=True, verbose_name="Код країни")
    flag_emoji = models.CharField(max_length=10, blank=True, verbose_name="Прапор")
    currency = models.CharField(max_length=10, blank=True, verbose_name="Валюта")

    class Meta:
        db_table = "geo_country"
        verbose_name = "Країна"
        verbose_name_plural = "Країни"
        ordering = ["name"]

        indexes = [
            GinIndex(fields=['name'], name='country_name_trgm_idx', opclasses=['gin_trgm_ops']),
            GinIndex(fields=['name_ua'], name='country_name_ua_trgm_idx', opclasses=['gin_trgm_ops']),
        ]

    def __str__(self):
        return f"{self.flag_emoji} {self.name}".strip()
