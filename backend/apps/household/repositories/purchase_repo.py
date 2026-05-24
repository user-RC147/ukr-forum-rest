from django.db import transaction

from apps.household.models.purchase import Purchase
from apps.household.models.purchase_item import PurchaseItem
from apps.household.models.product import Product
from apps.household.dto.purchase_dto import CreatePurchaseInDTO


class PurchaseRepo:
    """
    Репозиторій для роботи з чеками.
    Відповідає виключно за операції запису в базу даних (Команди).
    """

    def create_with_items(self,dto:CreatePurchaseInDTO,user_id:int)->Purchase:
        # Пояснення дії 1: Відкриваємо атомарну транзакцію
        with transaction.atomic():

            # Пояснення дії 2: Створюємо шапку чека
            purchase=Purchase.objects.create(
                asset_id=dto.asset_id,
                market_id=dto.market_id,
                data_purchase=dto.data_purchase,
                note=dto.note,
                created_by_id=user_id
            )

            # Пояснення дії 3: Збираємо назви товарів для текстового зліпку (Snapshot)
            product_ids=[item.product_id for item in dto.items]
            product_map={
                p.id:p.name for p in Product.objects.filter(id__in=product_ids)
            }

            # Пояснення дії 4: Готуємо масив моделей рядків чека
            items_to_create=[]
            for item in dto.items:
                product_name = product_map.get(item.product_id,"Невідомий товар")

                items_to_create.append(
                    PurchaseItem(
                        purchase=purchase,
                        product_id=item.product_id,
                        product_name_snapshot=product_name,  # Фіксуємо назву на момент покупки
                        quantity=item.quantity,
                        price_per_unit=item.price_per_unit
                    )
                )

        # Пояснення дії 5: Масове збереження рядків одним SQL-запитом
        if items_to_create:
            PurchaseItem.objects.bulk_create(items_to_create)

        return purchase