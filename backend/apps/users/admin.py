from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Додаємо нові колонки в загальний список
    list_display = (
        "username",
        "email",
        "get_location_display",
        "is_staff",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "country_id",
        "region_id",
        "city_id"
        )
    

    # Налаштовуємо сторінку редагування користувача
    fieldsets = UserAdmin.fieldsets + (
        (
            "Локація та Приватність",
            {
                "fields": (
                    "country",
                    "country_public",
                    "region",
                    "region_public",
                    "city",
                    "city_public",
                ),
                "description": "Налаштування географічного положення та відображення для інших користувачів.",
            },
        ),
    )

    # Додаємо можливість бачити локацію текстом прямо в списку
    def get_location_display(self, obj):
        # Перевірка, чи метод існує в моделі, щоб не "покласти" адмінку
        if hasattr(obj, 'get_location_display'):
            return obj.get_location_display()
        return "Не вказано"

    get_location_display.short_description = "Локація"
