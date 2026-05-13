from django.contrib.auth.models import AbstractUser
from django.db import models


from core.mixins.LocationMixin import PrivateLocationMixin
from apps.users.models.consent import ConsentText


class CustomUser(AbstractUser, PrivateLocationMixin):

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Ваш логін",
        help_text="Обов'язкове поле. Тільки літери, цифри та @/./+/-/_.",
    )

    display_name = models.CharField(
        max_length=100,
        verbose_name="Публічне ім'я (нікнейм)",
        blank=True,
        default="",
    )

    first_name_public = models.BooleanField(default=False)
    last_name_public  = models.BooleanField(default=False)

    age = models.PositiveIntegerField(blank=True, null=True)

    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )
    phone_public   = models.BooleanField(default=False)
    email_public   = models.BooleanField(default=False)

    social_network = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Соц.мережа"
    )
    social_public = models.BooleanField(default=False)

    # country_public, region_public, city_public
    # ← вже є в PrivateLocationMixin, не дублюємо

    consent_given = models.BooleanField(
        default=False, verbose_name="Згода на обробку даних"
    )
    consent_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата згоди"
    )
    consent_version = models.ForeignKey(
        ConsentText, null=True, blank=True, on_delete=models.SET_NULL
    )

    visibility = models.JSONField(default=dict)
    is_banned  = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_public_name(self):
        return self.display_name or self.username

    def get_public_first_name(self):
        return self.first_name if self.first_name_public else None

    def get_public_last_name(self):
        return self.last_name if self.last_name_public else None

    def get_public_email(self):
        return self.email if self.email_public else None

    def get_public_phone(self):
        return self.phone_number if self.phone_public else None

    def get_public_social(self):
        return self.social_network if self.social_public else None