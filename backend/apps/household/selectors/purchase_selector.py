from django.db.models import Q

from apps.household.dto.group_dto import (
    Group_id_user_OutDTO,
    GroupMemberOutDTO,
    GroupOutDTO,GroupMember_id_user_OutDTO
)
from apps.household.dto.purchase_dto import PurchaseItemOutDTO, Purchase_Id_Name_OutDTO
from apps.household.dto.asset_dto import AssetId_Name_OutDTO
from apps.household.dto.market_dto import Market_Id_Name_OutDTO
from apps.household.dto.product_dto import ProductOutDTO
from apps.household.dto.location_dto import Location_Id_InDTO
from apps.household.dto.unit_of_measure_dto import UnitOfMeasureOutDTO
from apps.household.dto.category_dto import CategoryOutDTO
from apps.household.dto.user_dto import User_Id_OutDTO

from apps.household.models.asset import Asset
from apps.household.models.category import Category
from apps.household.models.group import Group, GroupMember
from apps.household.models.market import Market
from apps.household.models.product import Product
from apps.household.models.purchase import Purchase
from apps.household.models.purchase_item import PurchaseItem
from apps.household.models.unit_of_measure import UnitOfMeasure


class PurchaseSelector:
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def get_all_purchase(self, user_id: int) -> list[Purchase_Id_Name_OutDTO]:
        
        purchase_list = Purchase.objects.filter(
            Q(asset__group__members__user_id=user_id) |
            Q(asset__group__created_by_id=user_id)
        ).select_related(
            "asset",
            "market",
            "asset__group",
            "asset__created_by",
            
        ).prefetch_related(
            "items",
            "asset__group__members",
            'items__product__unit_of_measure',
            'items__product__category'
        )

        print(purchase_list.count())
        print(list(purchase_list))

        dto_purchase_list = [_dto_purchase(purchase) for purchase in purchase_list]       

        return dto_purchase_list


def _dto_location(data) -> Location_Id_InDTO:
    return Location_Id_InDTO(
        country_id=data.country_id, region_id=data.region_id, city_id=data.city_id
    )


def _to_user(data: Purchase) -> User_Id_OutDTO:
    return User_Id_OutDTO(id=data.id)


def _to_group_members(data: GroupMember) -> GroupMember_id_user_OutDTO:
    return GroupMember_id_user_OutDTO(
        id=data.id,
        group_id=data.group_id,
        user_id=data.user_id,
        role=data.role,
        joined_at=data.joined_at,
    )


def _to_group(data: Group) -> Group_id_user_OutDTO:
    return Group_id_user_OutDTO(
        id=data.id,
        name=data.name,
        created_by_id=data.created_by_id,
        created_at=data.created_at,
        members=[_to_group_members(member) for member in data.members.all()],
    )


def _to_dto_asset(data: Asset) -> AssetId_Name_OutDTO:
    return AssetId_Name_OutDTO(
        id=data.id,
        name=data.name,
        group=_to_group(data.group),
        location=_dto_location(data),
        address_line=data.address_line,
        created_by_id=data.created_by_id,
        created_at=data.created_at,
    )


def _to_dto_market(data: Market) -> Market_Id_Name_OutDTO:
    return Market_Id_Name_OutDTO(
        id=data.id,
        name=data.name,
        address_line=data.address_line,
        location=_dto_location(data),
    )


def _to_unit(data: UnitOfMeasure) -> UnitOfMeasureOutDTO:
    return UnitOfMeasureOutDTO(id=data.id, name=data.name, code=data.code)


def _to_category(data: Category|None) -> CategoryOutDTO|None:

    if data:
        return CategoryOutDTO(
            id=data.id,
            name=data.name,
            icon=data.icon,
            is_active=data.is_active,
            parent_id=data.parent_id,
        )


def _to_product(data: Product) -> ProductOutDTO:
    return ProductOutDTO(
        id=data.id,
        name=data.name,
        unit_of_measure=_to_unit(data.unit_of_measure),
        created_by_id=data.created_by_id,
        category=_to_category(data.category),
    )


def _to_items_purchaseItem(data: PurchaseItem) -> PurchaseItemOutDTO:
    return PurchaseItemOutDTO(
        id=data.id,
        purchase_id=data.purchase_id,
        product=_to_product(data.product),
        quantity=data.quantity,
        price_per_unit=data.price_per_unit,
        total_price=data.total_price,
    )


def _dto_purchase(data: Purchase) -> Purchase_Id_Name_OutDTO:
    return Purchase_Id_Name_OutDTO(
        id=data.id,
        data_purchase=data.data_purchase,
        note=data.note,
        asset=_to_dto_asset(data.asset),
        market=_to_dto_market(data.market),
        created_at=data.created_at,
        created_by_id=data.created_by_id,
        items=[_to_items_purchaseItem(item) for item in data.items.all()],
        # Фінансовий підсумок чека
        total_amount=data.total_amount,  #
    )
