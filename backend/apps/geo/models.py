from django.db import models


class Country(models.Model):
    # Назва країни англійською (з API)
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Назва країни"
    )
    # Назва українською — заповнюємо вручну або потім
    name_ua = models.CharField(
        max_length=100, blank=True, default="", verbose_name="Назва українською"
    )
    # Код країни: UA, DE, PL
    code = models.CharField(
        max_length=5, unique=True, verbose_name="Код країни"
    )
    flag_emoji = models.CharField(
        max_length=10, blank=True, verbose_name="Прапор"
    )
    currency = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Валюта"
    )

    class Meta:
        db_table = "geo_country"
        verbose_name = "Країна"
        verbose_name_plural = "Країни"
        ordering = ["name"]

    def __str__(self):
        return f"{self.flag_emoji} {self.name}".strip()


class Region(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Назва регіону"
    )
    name_ua = models.CharField(
        max_length=100, blank=True, default="", verbose_name="Назва українською"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="regions",
        verbose_name="Країна",
    )
    # ID регіону з api.ukrkolo.site — для синхронізації
    api_id = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="ID в Geo API"
    )

    class Meta:
        db_table = "geo_region"
        verbose_name = "Регіон"
        verbose_name_plural = "Регіони"
        unique_together = ("name", "country")
        ordering = ["country__name", "name"]

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Назва міста"
    )
    name_ua = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Назва українською"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name="Країна",
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name="Регіон",
    )
    # ID міста з api.ukrkolo.site — для синхронізації
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