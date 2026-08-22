from django.conf import settings
from django.db import models


class ReferralCode(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Власник реф.коду",
    )
    code = models.CharField(
        max_length=40, unique=True, verbose_name="унікальний рядок, uuid4"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Коли створений код"
    )
    expires_at = models.DateTimeField(verbose_name="Кінцева дата використання коду")
    is_active = models.BooleanField(default=True, verbose_name="Активний/неактивний")
    max_uses = models.IntegerField(
        null=True, blank=True, verbose_name="Ліміт використання коду 1 або безліч"
    )
    used_count = models.IntegerField(
        default=0, verbose_name="Лічільник використання активного коду"
    )
