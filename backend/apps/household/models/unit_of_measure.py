from django.db import models


class UnitOfMeasure(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Код")

    name = models.CharField(max_length=20, verbose_name="Назва")

    class Meta:
        verbose_name = "Одиниця вимірювання"
        verbose_name_plural = "Одиниці вимірювання"
        ordering = ["name"]

    def __str__(self):
        return self.name
