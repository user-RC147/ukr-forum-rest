from apps.household.repositories.product_repo import ProductRepo
from apps.household.selectors.product_selector import ProductSelector
from apps.household.dto.product_dto import CreateProductInDTO
from apps.household.models.product import Product
from apps.household.dto.product_dto import CreateProductInDTO
from apps.household.exceptions import ProductNotFoundException, ProductAlreadyExistsException
from apps.users.exceptions import UserNotFoundException

from apps.users.contracts.user_contract import get_user_contract


class ProductService:

    def __init__(self)->None:
        self._repository=ProductRepo()
        self._selector=ProductSelector()
        self._user_contract=get_user_contract()

    def get_all_products(self,search_query:str=None)->list[Product]:
        return self._selector.get_product_list(search_query=search_query)
    
    
    def create(self,dto:CreateProductInDTO,user)->Product:
        # Тут за потреби можна додати валідацію (наприклад, перевірку на унікальність імені)
       
        owner_id=self._user_contract.get(user.id)
      
        existing_product=self._selector.find_product_by_name(dto.name)
        
        if existing_product is None:
            return self._repository.create(dto=dto,user_id=owner_id.id)
        else:
            raise ProductAlreadyExistsException(f"Product with name '{dto.name}' already exists.")