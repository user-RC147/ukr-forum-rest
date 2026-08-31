from typing import Any
from django.db import models
from django.conf import settings

from .category import Category



class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Найменування товару")

    unit_of_measure = models.ForeignKey(
        'UnitOfMeasure',
        on_delete=models.PROTECT,
        related_name='unit_products'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="cat_products"
    )

    created_by= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    create_date=models.DateField(auto_now_add=True,verbose_name="Дата створення товару")

    class Meta:
        verbose_name = "Товар"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.unit_of_measure})"

