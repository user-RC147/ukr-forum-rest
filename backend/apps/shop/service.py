from .models import ProductModel
from apps.shop.base.service_base import BaseService

class ProductService(BaseService[ProductModel]):
    def __init__(self, model=ProductModel):
        super().__init__(model)
    
    def get_all(self):
        return self.model.objects.all()