from django.db import models
from django.conf import settings

from apps.users.models.referral_code import ReferralCode


class ReferralUsage(models.Model):

    code = models.ForeignKey(
        ReferralCode,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Код яким скористались",
    )
    used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        unique=True,
        verbose_name="Хто скористався",
    )
    used_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Коли скористалися кодом"
    )
