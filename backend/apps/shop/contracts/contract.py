from apps.shop.contracts.dto import ProductDTO
from backend.apps.shop.contracts.protocols import ProductContractProtocol
from core.paginator.dto import PaginatorDTO

from ..service import ProductService


class ProductContract:
    def __init__(self, service: ProductService | None = None):
        self.service = service if service is not None else ProductService()
        self.dto_class = ProductDTO

    # set user_id value(with int type) for return owned products
    def get_all(self, user_id: int | None = None) -> PaginatorDTO[ProductDTO]:
        if user_id:
            data = self.service.get_all(user_id=user_id)
        else:
            data = self.service.get_all()
        return data

    def get_many(
        self, product_ids: list[int], page: int = 1, page_size: int = 20
    ) -> PaginatorDTO[ProductDTO]:
        return self.service.get_many(product_ids, page, page_size)


def get_product_contract() -> ProductContractProtocol:
    return ProductContract()
