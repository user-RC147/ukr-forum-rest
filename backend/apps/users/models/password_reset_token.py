from django.db import models
from django.conf import settings


class PasswordResetToken(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Кому належить токен",
    )
    token = models.CharField(
        max_length=40, unique=True, verbose_name="Одноразовий код скидання"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Коли створено")
    expires_at = models.DateTimeField(verbose_name="")
    is_used = models.BooleanField(
        default=False, verbose_name="Використаний/Невикористаний"
    )
