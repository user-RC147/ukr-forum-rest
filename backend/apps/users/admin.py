from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import PasswordResetToken, ReferralCode, ReferralUsage

from apps.users.models.user import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=('id','username','display_name')

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used',)


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'code', 'is_active', 'used_count', 'max_uses', 'expires_at')
    list_filter = ('is_active',)


@admin.register(ReferralUsage)
class ReferralUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'used_by', 'used_at')