from typing import Protocol, Optional
from apps.shop.dto import ProductDTO


class ProductContractProtocol(Protocol):
    # set user_id value(with int type) for return owned products
    def all_products(self, user_id: Optional[int]) -> ProductDTO: ...

    # user_id for validation user==owner
    def delete_product(self, id: int, user_id: int) -> None: ...
