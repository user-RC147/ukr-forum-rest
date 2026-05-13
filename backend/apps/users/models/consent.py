from django.db import models


class ConsentText(models.Model):
    version = models.CharField(max_length=10, verbose_name="Версія тексту")
    text = models.TextField(verbose_name="Текст погодження")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення тексту погодження"
    )

    def __str__(self):
        return f"{self.version}"