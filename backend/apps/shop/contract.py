from .dto import AllProductsDTO
from .service import ProductService

class ProductContract:
    def __init__(self):
        self.service = ProductService()

    def all_products_contract(self):
        data = self.service.get_all_products()
        return [self._to_dto(d) for d in data]
                        
    def _to_dto(self, product) -> AllProductsDTO:
        return AllProductsDTO(id=product.id, title=product.title, description=product.description, price=product.price)