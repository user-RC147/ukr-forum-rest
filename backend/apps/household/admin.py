from django.contrib import admin
from apps.household.models.asset import Asset
from apps.household.models.category import Category
from apps.household.models.group import Group, GroupMember
from apps.household.models.product import Product
from apps.household.models.purchase import Purchase
from apps.household.models.purchase_item import PurchaseItem
from apps.household.models.market import Market
from apps.household.models.unit_of_measure import UnitOfMeasure

# Імпортуємо ваш репозиторій для роботи з базою даних
from apps.household.repositories.group_repo import GroupRepo


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'address_line')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'created_by', 'created_at')

    def save_model(self, request, obj: Group, form, change):
        """
        Перехоплює збереження групи в адмінці.
        Якщо група створюється вперше (не редагується), пускаємо логіку через репозиторій.
        """
        if not change:  # change=False означає, що це саме створення нової групи
            # Викликаємо логіку вашого репозиторію, який створює і групу, і учасника-творця
            repo = GroupRepo()
            repo.create_group_with_creator(
                name=obj.name,
                creator_id=obj.created_by.id
            )
        else:
            # Якщо це просто редагування існуючої групи (наприклад, зміна назви), 
            # виконуємо стандартне збереження Django
            super().save_model(request, obj, form, change)


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('id','group', 'user', 'role', 'joined_at')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','name','group')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'parent', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'unit_of_measure','created_by')

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('id','code', 'name')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('asset', 'market', 'data_purchase', 'created_by', 'total_amount')


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'product_name_snapshot', 'quantity', 'price_per_unit', 'total_price')




# from django.contrib import admin
# from apps.household.models.asset import Asset
# from apps.household.models.category import Category
# from apps.household.models.group import Group,GroupMember
# from apps.household.models.product import Product
# from apps.household.models.purchase import Purchase
# from apps.household.models.purchase_item import PurchaseItem
# from apps.household.models.market import Market


# @admin.register(Market)
# class MarketAdmin(admin.ModelAdmin):
#     list_display=('name','address_line')


# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_by', 'created_at')


# @admin.register(GroupMember)
# class GroupMemberAdmin(admin.ModelAdmin):
#     list_display = ('group', 'user', 'role', 'joined_at')


# @admin.register(Asset)
# class AssetAdmin(admin.ModelAdmin):
#     list_display = ('name', 'group')


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'parent', 'is_active')


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'unit_of_measure')


# @admin.register(Purchase)
# class PurchaseAdmin(admin.ModelAdmin):
#     list_display = ('asset', 'market', 'data_purchase', 'created_by', 'total_amount')


# @admin.register(PurchaseItem)
# class PurchaseItemAdmin(admin.ModelAdmin):
#     list_display = ('purchase', 'product_name_snapshot', 'quantity', 'price_per_unit', 'total_price')
