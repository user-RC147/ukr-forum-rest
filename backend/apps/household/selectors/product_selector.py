from django.db.models import Q

from apps.household.dto.product_dto import CategoryProductOutDTO, ProductOutDTO
from apps.household.dto.unit_of_measure_dto import UnitOfMeasureOutDTO
from apps.household.models.product import Product
from apps.household.exceptions import ProductNotFoundException


class ProductSelector:

    def get_all_product(self)->list[ProductOutDTO]:
        products = Product.objects.select_related(
            'category',
            'unit_of_measure'
        ).distinct()
        
        return [ProductOutDTO(
            id=product.id,
            name=product.name,
            unit_of_measure=_dto_unit_out(product.unit_of_measure),
            created_by_id=product.created_by_id,
            category=_dto_category_out(product.category) if product.category else None,
        )for product in products]

         
         


    def get_product_by_name(self, name: str) -> Product:
        """Повертає товар за його назвою."""
       
        return Product.objects.get(name=name)
   

    def find_product_by_name(self, name: str) -> Product | None:
        """Повертає список товарів, які містять пошуковий запит у назві."""
        return Product.objects.filter(name=name).first()

def _dto_category_out(data)->CategoryProductOutDTO:
    return CategoryProductOutDTO(
        id=data.id,
        name=data.name,
        icon=data.icon,
        is_active=data.is_active,
        parent_id=data.parent_id
    )



def _dto_unit_out(data)->UnitOfMeasureOutDTO:
    return UnitOfMeasureOutDTO(
        id=data.id,
        name=data.name,
        code=data.code
    )
