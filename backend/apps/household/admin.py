from django.contrib import admin

from apps.household.models import Asset,Category,Group,GroupMember,PlaceType

@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    list_display=('name','group')

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display=('group','user','role','joined_at')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=('name','group','place_type')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','parent','is_active')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display=('name','created_by','created_at')

