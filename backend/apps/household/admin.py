from django.contrib import admin
from apps.household.models import (
    Asset, Category, Group, GroupMember,
    Product, Purchase, PurchaseItem
)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'role', 'joined_at')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit_of_measure')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('asset', 'market', 'data_purchase', 'created_by', 'total_amount')


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'product_name_snapshot', 'quantity', 'price_per_unit', 'total_price')