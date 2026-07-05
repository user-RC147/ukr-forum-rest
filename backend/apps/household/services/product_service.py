from tokenize import group
from apps.household.repositories.product_repo import ProductRepo
from apps.household.selectors.product_selector import ProductSelector
from apps.household.dto.product_dto import CreateProductInDTO
from apps.household.models.product import Product
from apps.household.dto.product_dto import CreateProductInDTO,ProductOutDTO
from apps.household.exceptions import ProductNotFoundException, ProductAlreadyExistsException
from apps.shop import serializers
from apps.shop.dto import ProductDTO
from apps.users.exceptions import UserNotFoundException


from apps.users.contracts.user_contract import get_user_contract


class ProductService:

    def __init__(self)->None:
        self._repository=ProductRepo()
        self._selector=ProductSelector()
        self._user_contract=get_user_contract()



    # def group_in_user_exsits(self):
    #     group_exsist = self._selector

    def get_all_products(self)->list[ProductOutDTO]:
        products = self._selector.get_all_product()

        return  products
    
    
    def create(self,dto:CreateProductInDTO,user_id:int)->Product:
        # Тут за потреби можна додати валідацію (наприклад, перевірку на унікальність імені)
       
        #owner_id=self._user_contract.get(user_id.id)
      
        existing_product=self._selector.find_product_by_name(dto.name)
        
        if existing_product is None:
            return self._repository.create(dto=dto,user_id=user_id)
        else:
            raise ProductAlreadyExistsException(f"Product with name '{dto.name}' already exists.")