from .dto import ProductDTO
from .service import ProductService


class ProductContract:
    def __init__(self):
        self.service = ProductService()

    def all_products_contract(self) -> list[ProductDTO]:
        data = self.service.get_all()
        return [self._to_dto(d) for d in data]

    def _to_dto(self, product) -> ProductDTO:
        return ProductDTO(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price,
        )
