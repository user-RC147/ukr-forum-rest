from django.db.models import Q

from apps.household.models.product import Product
from apps.household.exceptions import ProductNotFoundException


class ProductSelector:

    def get_product_list(self,search_query:str=None)->list[Product]:
        """Повертає список товарів з можливістю текстового пошуку."""
        queryset=Product.objects.all()
        if search_query:
            queryset=queryset.filter(name__icontains=search_query)
        return list(queryset.order_by('name'))
    
    def get_product_by_name(self,name:str)->Product:
        """Повертає товар за його назвою."""
        try:
            return Product.objects.get(name=name)
        except Product.DoesNotExist:
            raise ProductNotFoundException(f"Product with name '{name}' not found.")

    def find_product_by_name(self,name:str)->Product|None:
        """Повертає список товарів, які містять пошуковий запит у назві."""
        return Product.objects.filter(name=name).first()