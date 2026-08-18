from dataclasses import fields

from apps.shop.contracts.dto import ProductDTO
from backend.apps.shop.contracts.protocols import ProductContractProtocol

from ..service import ProductService


class ProductContract:
    def __init__(self):
        self.service = ProductService()
        self.dto_class = ProductDTO

    # set user_id value(with int type) for return owned products
    def all_products_contract(self, user_id=None) -> list[ProductDTO]:
        if user_id:
            data = self.service.get_all(int(user_id))
        else:
            data = self.service.get_all()
        return [self._to_dto(d) for d in data]

    def _to_dto(self, data) -> ProductDTO:
        dto_fields = {f.name for f in fields(self.dto_class)}
        result = {field: getattr(data, field) for field in dto_fields}
        return self.dto_class(**result)


def get_product_contract() -> ProductContractProtocol:
    return ProductContract()
