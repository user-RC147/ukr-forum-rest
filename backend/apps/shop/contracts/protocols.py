from typing import Protocol

from apps.shop.contracts.dto import ProductDTO
from core.paginator.dto import PaginatorDTO


class ProductContractProtocol(Protocol):
    # set user_id value(with int type) for return owned products
    def get_all(self, user_id: int | None) -> PaginatorDTO[ProductDTO]: ...


def get_many(
    self, product_ids: list[int], page: int, page_size: int
) -> PaginatorDTO[ProductDTO]: ...
