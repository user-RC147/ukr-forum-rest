from .models import ProductModel
from apps.shop.base.service_base import BaseService
from .exceptions import UnauthorizedException, GeoNotFound


import logging

logger = logging.getLogger("shop")


class ProductService(BaseService[ProductModel]):
    def __init__(self, model=ProductModel):
        super().__init__(model)

    def get_all(self, user_id=None):
        if user_id:
            return self.model.objects.all().filter(owner_id=user_id)

        return self.model.objects.all()

    def create(self, user_id: int, data: dict) -> ProductModel:
        if data["country_id"] == 2 or not data["city_id"] or not data["region_id"]:
            logger.info("Geo data with country: %s, region: %s, city: %s not found!", data["country_id"], data["region_id"], data["city_id"])
            raise GeoNotFound("Geo data with this params not found!")

        data["owner_id"] = user_id
        return super().create(data)

    def update(self, id: int, user_id: int, data: dict) -> ProductModel:
        product = self.get(id)
        if int(user_id) == product.owner_id:
            return super().update(id, data)
        else:
            logger.warning(
                "Access denied to product id: %s with user_id: %s", product.id, user_id
            )
            raise UnauthorizedException

    def delete(self, id: int, user_id: int) -> None:

        product = self.get(id)
        if int(user_id) == product.owner_id:
            return super().delete(id)
        else:
            logger.warning(
                "Access denied to product id: %s with user_id: %s", product.id, user_id
            )
            raise UnauthorizedException
