from django.db.models import Q

from apps.household.dto.product_dto import ProductOutDTO
from apps.household.dto.purchase_dto import PurchaseItemOutDTO
from apps.household.dto.unit_of_measure_dto import UnitOfMeasureOutDTO
from apps.household.models.product import Product
from apps.household.models.purchase_item import PurchaseItem
from apps.household.models.unit_of_measure import UnitOfMeasure
from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate


class PurchaseItemSelector:
    def get_all_purchase_item(
        self,
        user_id: int,
        page: int,
        page_size: int,
        date_from: str | None,
        date_to: str | None,
    ) -> PaginatorDTO[PurchaseItemOutDTO]:

        purchase_items = (
            PurchaseItem.objects.filter(
                Q(purchase__asset__group__members__user_id=user_id)
                | Q(purchase__asset__group__created_by_id=user_id)
            )
            .select_related(
                "purchase",
                "product",
                "product__unit_of_measure",
            )
            .distinct().order_by('-purchase__data_purchase')
        )

        if date_to and date_from:
            purchase_items = purchase_items.filter(
                purchase__data_purchase__gte=date_from,
                purchase__data_purchase__lte=date_to,
            )

        count = purchase_items.count()

        offset = (page - 1) * page_size
        page_items = purchase_items[offset : offset + page_size]

        dto = [_to_dto_purchase_item(item) for item in page_items]

        paginator_pages = paginate(dto, count, page, page_size)

        return paginator_pages


def _to_dto_unit(data: UnitOfMeasure) -> UnitOfMeasureOutDTO:
    return UnitOfMeasureOutDTO(id=data.id, name=data.name, code=data.code)


def _to_dto_product(data: Product) -> ProductOutDTO:
    return ProductOutDTO(
        id=data.id,
        name=data.name,
        unit_of_measure=_to_dto_unit(data.unit_of_measure),
        created_by_id=data.created_by_id,
    )


def _to_dto_purchase_item(data: PurchaseItem) -> PurchaseItemOutDTO:
    return PurchaseItemOutDTO(
        id=data.id,
        purchase_id=data.purchase_id,
        product=_to_dto_product(data.product),
        quantity=data.quantity,
        price_per_unit=data.price_per_unit,
        total_price=data.total_price,
    )
