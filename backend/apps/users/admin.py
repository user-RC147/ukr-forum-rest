from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models.user import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=('id','username','display_name')