import dataclasses
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import QuerySet

from apps.files.contracts import get_file_contract
from apps.geo.contracts.city_contract import get_city_contract
from apps.geo.contracts.country_contract import get_country_contract
from apps.geo.contracts.region_contract import get_region_contract
from apps.shop.base.service_base import BaseService

from .exceptions import GeoNotFound, UnauthorizedException
from .models import ProductModel

logger = logging.getLogger("shop")


class ProductService(BaseService[ProductModel]):
    def __init__(self, model=ProductModel) -> None:
        super().__init__(model)
        self.country_service = get_country_contract()
        self.region_service = get_region_contract()
        self.city_service = get_city_contract()
        self.file_contract = get_file_contract()

    def get(self, id: int) -> ProductModel:
        result = super().get(id)

        if not result:
            return result

        files_map = {}
        if result.files_ids:
            files_map = self.file_contract.get_many(result.files_ids)

        result.files = [
            dataclasses.asdict(files_map[fid])
            for fid in (result.files_ids or [])
            if fid in files_map
        ]

        geo = {
            "country": self.country_service.get_country(result.country_id)
            if result.country_id
            else None,
            "region": self.region_service.get_region(
                result.region_id, result.country_id
            )
            if result.region_id and result.country_id
            else None,
            "city": self.city_service.get_city(result.city_id, result.region_id)
            if result.region_id and result.city_id
            else None,
        }

        result.country = dataclasses.asdict(geo["country"])
        result.region = dataclasses.asdict(geo["region"])
        result.city = dataclasses.asdict(geo["city"])

        return result

    def get_all(self, user_id=None, page: int = 1, page_size: int = 20):
        qs = (
            self.model.objects.filter(owner_id=user_id)
            if user_id
            else self.model.objects.all()
        )

        result = list(qs)

        if not result:
            return result

        all_file_ids = []
        for r in result:
            if r.files_ids:
                all_file_ids.extend(r.files_ids)

        files_map = {}
        if all_file_ids:
            files_map = self.file_contract.get_many(all_file_ids)

        for r in result:
            r.files = [
                dataclasses.asdict(files_map[fid])
                for fid in (r.files_ids or [])
                if fid in files_map
            ]

        result = Paginator(result, page_size)

        return result.page(page).object_list

    def create(self, user_id: int, data: dict) -> ProductModel:
        self.geo_validate(data)

        data["owner_id"] = user_id
        files = data.pop("files")
        file_list = self.file_contract.create_many(files, user_id)
        file_ids = [i.id for i in file_list]
        data["files_ids"] = file_ids
        return super().create(data)

    def update(self, id: int, user_id: int, data: dict) -> ProductModel:
        self.geo_validate(data)
        product = self.get(id)
        if int(user_id) == product.owner_id:
            with transaction.atomic():
                files = data.pop("files")
                target_ids = product.files_ids
                self.file_contract.update_many(files, user_id, target_ids)
                return super().update(id, data)
        else:
            logger.warning(
                "Access denied to product id: %s with user_id: %s", product.id, user_id
            )
            raise UnauthorizedException

    def delete(self, id: int, user_id: int) -> None:

        product = self.get(id)
        if int(user_id) == product.owner_id:
            with transaction.atomic():
                self.file_contract.delete_many(product.files_ids)
                result = super().delete(id)
        else:
            logger.warning(
                "Access denied to product id: %s with user_id: %s", product.id, user_id
            )
            raise UnauthorizedException

        return result

    def nullify_geo(self, field_name: str, geo_id: int) -> int:

        return self.model.objects.filter(**{field_name: geo_id}).update(
            **{field_name: None}
        )

    def geo_validate(self, data: dict) -> None:
        try:
            country = self.country_service.get_country(data["country_id"])
            region = self.region_service.get_region(
                data["region_id"], data["country_id"]
            )
            city = self.city_service.get_city(data["city_id"], data["region_id"])
        except ObjectDoesNotExist:
            logger.info(
                "Geo data with country: %s, region: %s, city: %s not found!",
                data["country_id"],
                data["region_id"],
                data["city_id"],
            )
            raise GeoNotFound("Geo data with this params not found!")

    def delete_all_by_user(self, user_id: int) -> int:
        deleted, _ = self.model.objects.filter(owner_id=user_id).delete()
        return deleted

    @staticmethod
    def get_searchable_queryset() -> QuerySet[ProductModel]:
        return ProductModel.objects.filter(
            visible=True,
        )


def get_service() -> ProductService:
    return ProductService()
