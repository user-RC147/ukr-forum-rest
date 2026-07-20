from dataclasses import fields
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.manager import BaseManager

from .dto import ProductRepoDTO
from .exceptions import ProductNotFoundError
from .models import ProductModel

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(self) -> None:
        self.model = ProductModel

    def _get_model(self, id: int) -> ProductModel:
        try:
            return self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            raise ProductNotFoundError(extra={"product_id": id, "event": "get_product"})

    def get(self, id: int) -> ProductRepoDTO:
        result = self._get_model(id)
        return _to_dto(result)

    def get_many(
        self, user_id: int | None = None, limit: int = 100
    ) -> list[ProductRepoDTO]:
        if user_id:
            result = self.model.objects.filter(owner_id=user_id)
        else:
            result = self.model.objects.all()
        return [_to_dto(r) for r in result]

    def create(self, data: dict) -> ProductRepoDTO:
        result = self.model.objects.create(**data)
        return _to_dto(result)

    def update(self, id: int, data: dict) -> ProductRepoDTO:
        product = self._get_model(id)

        for field, value in data.items():
            setattr(product, field, value)

        product.save(update_fields=list(data.keys()))
        return _to_dto(product)

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


def _to_dto(data: ProductModel) -> ProductRepoDTO:
    dto_fields = {f.name for f in fields(ProductRepoDTO)}
    result = {field: getattr(data, field) for field in dto_fields}
    return ProductRepoDTO(**result)


def get_repo():
    return ProductRepository()
