from django.db import transaction

from apps.household.dto.asset_dto import AssetId_Name_OutDTO
from apps.household.dto.group_dto import (
    Group_Id_Name_OutDTO,
    Group_id_user_OutDTO,
    GroupOutDTO,
    GroupMemberOutDTO,
)
from apps.household.dto.location_dto import (
    CityNameOutDTO,
    CountryNameOutDTO,
    LocationId_Name_OutDTO,
    RegionNameOutDTO,
)

from core.dto.geo.location_dto import LocationOutDTO,Location_Id_InDTO,Location_Id_OutDTO,LocationShortOutDTO



from apps.household.dto.unit_of_measure_dto import UnitOfMeasureOutDTO
from apps.household.dto.market_dto import Market_Id_Name_OutDTO
from apps.household.dto.product_dto import CategoryProductOutDTO, ProductOutDTO
from apps.household.dto.purchase_dto import (
    Purchase_Id_OutDTO,
    PurchaseItemOutDTO,
    CreatePurchaseInDTO,
    PurchaseOutDTO,
    Purchase_Id_Name_OutDTO,
    PurchaseItemInDTO,
)

from apps.household.models.purchase import Purchase
from apps.household.models.purchase_item import PurchaseItem
from apps.household.models.product import Product

from apps.household.repositories.purchase_item_repo import PurchaseItemRepo


class PurchaseRepo:
    """
    Репозиторій для роботи з чеками.
    Відповідає виключно за операції запису в базу даних (Команди).
    """

    def get_location_id_name(self, item):
        location_id_name = LocationId_Name_OutDTO(
            country=CountryNameOutDTO(
                id=item.country.id,
                name=item.country.name,
                code=item.country.code,
            ),
            region=RegionNameOutDTO(
                id=item.region.id,
                name=item.region.name,
                name_ua=item.region.name_ua,
            ),
            city=CityNameOutDTO(
                id=item.city.id,
                name=item.city.name,
                name_ua=item.city.name_ua,
            ),
        )

        return location_id_name

    def create(self, dto: CreatePurchaseInDTO, creator_user_id: int) -> Purchase_Id_OutDTO:
        
        with transaction.atomic():
            create_purchase = Purchase.objects.create(
                asset_id=dto.asset_id,
                market_id=dto.market_id,
                data_purchase=dto.data_purchase,
                created_by_id=creator_user_id,
                note=dto.note,
            )
            PurchaseItemRepo().create_items_for_repo_purchase(
                dto=dto.items, purchase_id=create_purchase.id
            )

        purchase_id_obj = Purchase.objects.select_related(
            "asset",
            "market"
            ).prefetch_related(
                'items__product__unit_of_measure',
                'items__product__category'
            ).get(id=create_purchase.id)
        
        dto = _to_dto_new_purchase_out(purchase_id_obj)
       

        return dto


# def _to_dto_asset_out(data)->AssetOutDTO:
#     return AssetOutDTO()

# def _to_dto_market_out(data)->MarketFullOutDTO:
#     return MarketFullOutDTO()


def _to_dto_unit_out(data) -> UnitOfMeasureOutDTO:
    return UnitOfMeasureOutDTO(id=data.id, name=data.name, code=data.code)


def _to_dto_category_out(data) -> CategoryProductOutDTO:
    return CategoryProductOutDTO(
        id=data.id,
        name=data.name,
        icon=data.icon,
        is_active=data.is_active,
        parent_id=data.parent_id,
    )


def _to_dto_product_out(data) -> ProductOutDTO:
    return ProductOutDTO(
        id=data.id,
        name=data.name,
        unit_of_measure=_to_dto_unit_out(data.unit_of_measure),
        created_by_id=data.created_by_id,
        category=_to_dto_category_out(data.category) if data.category else None,
    )


def _to_dto_item_purchase_out(data) -> PurchaseItemOutDTO:
    return PurchaseItemOutDTO(
        id=data.id,
        purchase_id=data.purchase_id,
        product=_to_dto_product_out(data.product),
        quantity=data.quantity,
        price_per_unit=data.price_per_unit,
        total_price=data.total_price,
    )


def _to_dto_new_purchase_out(data) -> Purchase_Id_OutDTO:
    return Purchase_Id_OutDTO(
        id=data.id,
        data_purchase=data.data_purchase,
        note=data.note,
        asset_id=data.asset_id,
        market_id=data.market_id,
        created_at=data.created_at,
        created_by_id=data.created_by_id,
        items=[_to_dto_item_purchase_out(item) for item in data.items.all()],
        total_amount=data.total_amount,
    )
