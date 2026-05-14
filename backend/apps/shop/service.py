from .models import ProductModel
from .dto import AllProductsDTO
from apps.shop.base.service_base import BaseService
import logging

logger = logging.getLogger(__name__)

class ProductService(BaseService[ProductModel]):
    def __init__(self, model=ProductModel):
        super().__init__(model)
    
    def get_all(self):
        return self.model.objects.all()

    # def get(self, id: int):
    #     try:
    #         super().get(id)
    #     except self.model.DoesNotExist:
    #         logger.warning("Product not found in DB: pk=%s", id)
    #         raise ProductNotFound(f"Product {pk} not found")