from django.db import models
from django.conf import settings


class EmailConfirmationToken(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Кому належить токен",
    )
    token = models.CharField(
        max_length=40, unique=True, verbose_name="Одноразовий код підтвердження email"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Коли створено")
    expires_at = models.DateTimeField(verbose_name="Коли токен стає недійсним")
    is_used = models.BooleanField(
        default=False, verbose_name="Використаний/Невикористаний"
    )