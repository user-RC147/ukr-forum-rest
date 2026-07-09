from django.db.models import Q

from apps.household.dto.product_dto import CategoryProductDTO, ProductOutDTO
from apps.household.dto.unit_of_measure_dto import UnitOfMeasureDTO
from apps.household.models.product import Product
from apps.household.exceptions import ProductNotFoundException


class ProductSelector:

    def get_all_product(self)->list[ProductOutDTO]:
        products = Product.objects.select_related(
            "category", "unit_of_measure", "created_by").all()

        dto: list[ProductOutDTO] = [
            ProductOutDTO(
                id=product.id,
                name=product.name,
                unit_of_measure=UnitOfMeasureDTO(
                    id=product.unit_of_measure.id,
                    name=product.unit_of_measure.name,
                    code=product.unit_of_measure.code,
                ),
                created_by=product.created_by,
                category=(
                    CategoryProductDTO(
                        id=product.category.id,
                        name=product.category.name,
                        icon=product.category.icon,
                        is_active=product.category.is_active,
                        parent=product.category.parent_id,
                    )
                    if product.category
                    else None
                ),
            )
            for product in products
        ]
        return dto

    # def get_product_list(self,search_query:str=None)->list[Product]:
    #     """Повертає список товарів з можливістю текстового пошуку."""
    #     queryset=Product.objects.all()

    #     if search_query:
    #         queryset=queryset.filter(name__icontains=search_query)
    #     return list(queryset.order_by('name'))

    def get_product_by_name(self, name: str) -> Product:
        """Повертає товар за його назвою."""
        try:
            return Product.objects.get(name=name)
        except Product.DoesNotExist:
            raise ProductNotFoundException(f"Product with name '{name}' not found.")

    def find_product_by_name(self, name: str) -> Product | None:
        """Повертає список товарів, які містять пошуковий запит у назві."""
        return Product.objects.filter(name=name).first()
