from django.db import models
from django.conf import settings

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
   


    created_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← завжди вказує на активну модель користувача
        on_delete=models.CASCADE,
        null=True,      # ← додати тимчасово
        blank=True,     # ← додати тимчасово
        verbose_name="Створив",
    )
   
    created_at=models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
        )

    class Meta:
        db_table = "household_asset"
        verbose_name = "Актив"
        verbose_name_plural = "Активи"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.group.name})"