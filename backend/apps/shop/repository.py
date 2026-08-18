from dataclasses import fields
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.manager import BaseManager

from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate

from .dto import ProductRepoDTO
from .contracts.exceptions import ProductNotFoundError
from .models import ProductModel
from .ports import ProductRepositoryPort

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(self, model=ProductModel) -> None:
        self.model = model

    def _get_model(self, id: int) -> ProductModel:
        try:
            return self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            raise ProductNotFoundError(extra={"product_id": id, "event": "get_product"})

    def get(self, id: int) -> ProductRepoDTO:
        result = self._get_model(id)
        return _to_dto_product(result)

    def get_many(
        self,
        page: int,
        page_size: int = 20,
        user_id: int | None = None,
        product_ids: list[int] | None = None,
    ) -> PaginatorDTO:
        if product_ids:
            qs = self.model.objects.filter(id__in=product_ids)
        else:
            qs = self.model.objects.all()

        if user_id:
            qs = qs.filter(owner_id=user_id)
        qs = qs.order_by("id")

        offset = (page - 1) * page_size
        total = qs.count()
        items = list(qs[offset : offset + page_size])

        items = [_to_dto_product(i) for i in items]

        return paginate(items, total, page, page_size)

    def create(self, data: dict) -> ProductRepoDTO:
        result = self.model.objects.create(**data)
        return _to_dto_product(result)

    def update(self, id: int, data: dict) -> ProductRepoDTO:
        product = self._get_model(id)

        for field, value in data.items():
            setattr(product, field, value)

        product.save(update_fields=list(data.keys()))
        return _to_dto_product(product)

    def delete(self, id: int) -> None:
        self._get_model(id).delete()

    def delete_by_user(self, user_id: int) -> int:
        deleted, _ = self.model.objects.filter(owner_id=user_id).delete()
        return deleted

    def nullify_geo(self, field_name: str, geo_id: int) -> int:

        return self.model.objects.filter(**{field_name: geo_id}).update(
            **{field_name: None}
        )

    def searchable_queryset(self) -> BaseManager[ProductModel]:
        return self.model.objects.filter(
            visible=True,
        )


def _to_dto_product(data: ProductModel) -> ProductRepoDTO:
    dto_fields = {f.name for f in fields(ProductRepoDTO)}
    result = {field: getattr(data, field) for field in dto_fields}
    return ProductRepoDTO(**result)


def get_repo() -> ProductRepositoryPort:
    return ProductRepository()
