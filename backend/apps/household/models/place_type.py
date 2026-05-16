from django.db import models
from apps.household.models.group import Group



class PlaceType(models.Model):
    """
    Тип об'єкта витрат — створюється користувачем, належить групі.
    Наприклад: Дім, Дача, Авто, Готель.
    """
    name=models.CharField(
        max_length=100,
        verbose_name="Назва типу",
    )
    group=models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="place_types",
        verbose_name="Група",
    )

    class Meta:
        db_table="household_place_type"
        verbose_name="Тип об'єкта"
        verbose_name_plural="Типи об'єктів"
        unique_together=("name","group")
        ordering=["name"]

    def __str__(self):
        return f"{self.name} ({self.group.name})"