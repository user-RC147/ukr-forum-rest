from django.db import models
from django.conf import settings

from .category import Category



class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Найменування товару")

    # Одиниця вимірювання
    UNIT_CHOICES = [
        ('шт', 'Штуки (шт)'),
        ('кг', 'Кілограми (кг)'),
        ('г', 'Грами (г)'),
        ('л', 'Літри (л)'),
        ('мл', 'Мілілітри (мл)'),
        ('м', 'Метри (м)'),
        ('уп', 'Упаковка (уп)'),
        ('кор', 'Коробка (кор)'),
    ]

    unit_of_measure = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='шт',
        verbose_name="Одиниця вимірювання",
        help_text="В якій одиниці продається товар"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="products"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Товар"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.unit_of_measure})"

