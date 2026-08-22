from django.db import models
from django.contrib.auth.models import AbstractUser

from core.mixins.LocationMixin import PrivateLocationMixin

from apps.users.models.consent import ConsentText


class CustomUser(AbstractUser, PrivateLocationMixin):

    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Ваш логін",
        help_text="Обов'язкове поле. Тільки літери, цифри та @/./+/-/_.",
    )
    display_name = models.CharField(max_length=100, verbose_name="Публічне ім'я")

    first_name_public = models.BooleanField(default=False)
    last_name_public = models.BooleanField(default=False)

    email_public = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name="Дата народження"
    )
    date_of_birth_public = models.BooleanField(default=False)

    phone_number = models.CharField(
        max_length=50, blank=True, verbose_name="Ваш тел.номер"
    )
    phone_public = models.BooleanField(default=False)

    social_network = models.CharField(
        max_length=50, blank=True, verbose_name="Ваша соц.мережа"
    )
    social_public = models.BooleanField(default=False)

    is_banned = models.BooleanField(default=False)

    deletion_scheduled_at = models.DateTimeField(null=True, blank=True)

    consent_given = models.BooleanField(default=False, verbose_name="Погодження")
    consent_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата погодження"
    )
    consent_version = models.ForeignKey(
        ConsentText, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.username}"
