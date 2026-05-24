from apps.household.models.product import Product
from apps.household.dto.product_dto import CreateProductInDTO


class ProductRepo:

    def create(self,dto:CreateProductInDTO,user_id:int)->Product:
        """Створює новий товар у базі даних."""
        product = Product.objects.create(
            name=dto.name,
            unit_of_measure=dto.unit_of_measure,
            category_id=dto.category_id,
            created_by_id=user_id,
        )