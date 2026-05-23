from .models import ProductModel
from apps.shop.base.service_base import BaseService
from .exceptions import UnauthorizedException, GeoNotFound
from apps.geo.contracts.country_contract import get_country_contract
from apps.geo.contracts.region_contract import get_region_contract
from apps.geo.contracts.city_contract import get_city_contract

import logging

logger = logging.getLogger("shop")


class ProductService(BaseService[ProductModel]):
    def __init__(self, model=ProductModel) -> None:
        super().__init__(model)
        self.country_service = get_country_contract()
        self.region_service = get_region_contract()
        self.city_service = get_city_contract()

    def get_all(self, user_id=None):
        if user_id:
            return self.model.objects.all().filter(owner_id=user_id)

        return self.model.objects.all()

    def create(self, user_id: int, data: dict) -> ProductModel:
        if (
            not self.country_service.get_country(data["country_id"])
            or not self.region_service.get_region(data["region_id"], data["country_id"])
            or not self.city_service.get_city(data["city_id"], data["region_id"])
        ):
            logger.info(
                "Geo data with country: %s, region: %s, city: %s not found!",
                data["country_id"],
                data["region_id"],
                data["city_id"],
            )
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
