from collections.abc import Iterable
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.manager import BaseManager

from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate

from .contracts.exceptions import ProductNotFoundError
from .dto import ProductRepoDTO
from .models import ProductFileModel, ProductModel
from .ports import ProductRepositoryPort

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(self, model=ProductModel, file_model=ProductFileModel) -> None:
        self.model = model
        self.file_model = file_model

    def _get_model(self, id: int) -> ProductModel:
        try:
            return self.model.objects.prefetch_related("files").get(id=id)
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
        product_ids: Iterable[int] | None = None,
    ) -> PaginatorDTO:
        if product_ids:
            qs = self.model.objects.filter(id__in=product_ids).prefetch_related("files")
        else:
            qs = self.model.objects.all().prefetch_related("files")

        if user_id:
            qs = qs.filter(owner_id=user_id)
        qs = qs.order_by("id")

        offset = (page - 1) * page_size
        total = qs.count()
        items = list(qs[offset : offset + page_size])

        items = [_to_dto_product(i) for i in items]

        return paginate(items, total, page, page_size)

    def create(self, data: dict) -> ProductRepoDTO:
        file_ids = data.pop("file_ids", [])
        result = self.model.objects.create(**data)
        self.file_model.objects.bulk_create(
            [self.file_model(product=result, file_id=fid) for fid in file_ids]
        )
        return _to_dto_product(result)

    def update(self, id: int, data: dict) -> ProductRepoDTO:
        file_ids = data.pop("file_ids", [])
        product = self._get_model(id)

        for field, value in data.items():
            setattr(product, field, value)
        product.save(update_fields=list(data.keys()))

        if file_ids is not None:
            self._sync_files(product, file_ids)

        product.save(update_fields=list(data.keys()))
        return _to_dto_product(product)

    def _sync_files(self, product: ProductModel, new_file_ids: list[int]) -> None:
        current_file_ids = set(
            product.files.values_list("file_id", flat=True)
        )
        new_file_ids = set(new_file_ids)

        to_remove = current_file_ids - new_file_ids
        to_add = new_file_ids - current_file_ids

        if to_remove:
            product.files.filter(file_id__in=to_remove).delete()

        if to_add:
            self.file_model.objects.bulk_create(
                [self.file_model(product=product, file_id=fid) for fid in to_add]
            )

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
        ).prefetch_related("files")


def _to_dto_product(data: ProductModel) -> ProductRepoDTO:
    return ProductRepoDTO(
        id=data.id,
        owner_id=data.owner_id,
        title=data.title,
        description=data.description,
        created_at=data.created_at,
        country_id=data.country_id,
        region_id=data.region_id,
        city_id=data.city_id,
        category_id=data.category_id,
        price=data.price,
        visible=data.visible,
        file_ids=list(data.files.values_list("file_id", flat=True)),
        status=data.status,
    )


def get_repo() -> ProductRepositoryPort:
    return ProductRepository()
