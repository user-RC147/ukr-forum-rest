from typing import Protocol

from django.db.models.manager import BaseManager

from core.paginator.dto import PaginatorDTO

from .dto import ProductRepoDTO
from .models import ProductModel


class ProductRepositoryPort(Protocol):
    def get_many(
        self,
        page: int,
        page_size: int = 20,
        user_id: int | None = None,
        product_ids: list[int] | None = None,
    ) -> PaginatorDTO: ...

    def get(self, id: int) -> ProductRepoDTO: ...

    def create(self, data: dict) -> ProductRepoDTO: ...

    def update(self, id: int, data: dict) -> ProductRepoDTO: ...

    def delete(self, id: int) -> None: ...

    def delete_by_user(self, user_id: int) -> int: ...

    def nullify_geo(self, field_name: str, geo_id: int) -> int: ...

    def searchable_queryset(self) -> BaseManager[ProductModel]: ...
