from django.db import transaction

from apps.household.dto.purchase_dto import CreatePurchaseInDTO, PurchaseItemInDTO
from apps.household.models.purchase_item import PurchaseItem



class PurchaseItemRepo:

    def create_items_for_repo_purchase(self,dto:list[PurchaseItemInDTO],purchase_id:int):

        with transaction.atomic():
            items = [PurchaseItem(
                purchase_id=purchase_id,
                product_id = item.product_id,
                quantity=item.quantity,
                price_per_unit=item.price_per_unit,
            ) for item in dto
            ]

            create_purchase_item = PurchaseItem.objects.bulk_create(items)

        return create_purchase_item