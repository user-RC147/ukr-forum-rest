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
    LocationIdOutDTO,
    RegionNameOutDTO,
)
from apps.household.dto.market_dto import Market_Id_Name_OutDTO
from apps.household.dto.product_dto import CategoryProductDTO, ProductOutDTO
from apps.household.dto.purchase_dto import (
    PurchaseItemOutDTO,
    CreatePurchaseInDTO,
    PurchaseOutDTO,
    Purchase_Id_Name_OutDTO,
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

    def create(self, dto: CreatePurchaseInDTO, creator_user_id: int) -> bool:

        with transaction.atomic():
            create_purchase = Purchase.objects.create(
                asset_id=dto.asset_id,
                market_id=dto.market_id,
                data_purchase=dto.data_purchase,
                created_by_id=creator_user_id,
                note=dto.note,
            )
            PurchaseItemRepo().create_items_for_repo_purchase(dto=dto.items, purchase_id=create_purchase.id)

            # Оновлюємо об'єкт з бази, щоб отримати актуальний total_amount

        

        return True
