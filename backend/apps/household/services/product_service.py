from apps.household.repositories.product_repo import ProductRepo
from apps.household.selectors.product_selector import ProductSelector
from apps.household.dto.product_dto import CreateProductInDTO
from apps.household.models.product import Product


class ProductService:

    def __init__(self,repository:ProductRepo,selector:ProductSelector)->None:
        self._repository=repository
        self._selector=selector

    def get_all_products(self,search_query:str=None)->list[Product]:
        return self._selector.get_product_list(search_query=search_query)
    
    def create(self,dto:CreateProductInDTO,user)->Product:
        # Тут за потреби можна додати валідацію (наприклад, перевірку на унікальність імені)
        return self._repository.create(dto=dto,user_id=user.id)