from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "location_display",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Локація та Приватність",
            {
                "fields": (
                    "country_id",
                    "country_public",
                    "region_id",
                    "region_public",
                    "city_id",
                    "city_public",
                ),
                "description": "Налаштування географічного положення.",
            },
        ),
    )

    def location_display(self, obj):
        if hasattr(obj, 'get_location_display'):
            return obj.get_location_display()
        return "Не вказано"

    location_display.short_description = "Локація"