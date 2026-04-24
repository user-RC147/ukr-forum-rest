from django.contrib.auth.models import AbstractUser
from django.db import models



class ConsentText(models.Model):
    version = models.CharField(max_length=10, verbose_name="Версія тексту")
    text = models.TextField(verbose_name="Текст погодження")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення тексту погодження"
    )

    def __str__(self):
        return f"{self.version}"


class CustomUser(AbstractUser):

    # Перевизначаємо вбудоване поле username
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Ваш логін",  # Твоя нова назва
        help_text="Обов'язкове поле. Тільки літери, цифри та @/./+/-/_.",
    )

    # Те, що бачать люди
    display_name = models.CharField(
        max_length=100,
        verbose_name="Публічне ім'я (нікнейм)",
        blank=True,  # Дозволяє не заповнювати поле у формах
        default="",  # Гарантує, що в базі не буде NULL
    )

    first_name_public = models.BooleanField(default=False)
    last_name_public = models.BooleanField(default=False)

    age = models.PositiveIntegerField(blank=True, null=True)

    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )
    phone_public = models.BooleanField(default=False)

    email_public = models.BooleanField(default=False)

    social_network = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Соц.мережа"
    )
    social_public = models.BooleanField(default=False)

   
    country_public = models.BooleanField(default=False)

  
    region_public = models.BooleanField(default=False)

   
    city_public = models.BooleanField(default=False)

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
    is_banned = models.BooleanField(default=False)
