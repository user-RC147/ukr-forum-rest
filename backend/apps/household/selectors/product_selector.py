from django.db.models import Q

from apps.household.models.product import Product


class ProductSelector:

    def get_product_list(self,search_query:str=None)->list[Product]:
        """Повертає список товарів з можливістю текстового пошуку."""
        queryset=Product.objects.all()
        if search_query:
            queryset=queryset.filter(name__icontains=search_query)
        return list(queryset.order_by('name'))