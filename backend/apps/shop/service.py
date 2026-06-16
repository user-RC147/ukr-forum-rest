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
        self.country_contract = get_country_contract()
        self.region_contract = get_region_contract()
        self.city_contract = get_city_contract()
        self.file_contract = get_file_contract()

    def _fetch_map(self, ids: list, contract) -> dict:
        """Deduplicate IDs and call get_many."""
        unique_ids = list(set(filter(None, ids)))  # take away None and doubles
        if not unique_ids:
            return {}
        return contract.get_many(unique_ids)

    @staticmethod
    def _to_dict(obj) -> dict | None:
        return dataclasses.asdict(obj) if obj is not None else None

    def _attach_products(self, products: list) -> None:
        # Get all IDs
        all_file_ids, all_city_ids, all_region_ids, all_country_ids = [], [], [], []

        for p in products:
            all_file_ids.extend(p.files_ids or [])
            all_city_ids.append(p.city_id)
            all_region_ids.append(p.region_id)
            all_country_ids.append(p.country_id)

        # Patter for all contracts
        files_map    = self._fetch_map(all_file_ids,    self.file_contract)
        cities_map   = self._fetch_map(all_city_ids,    self.city_contract)
        regions_map  = self._fetch_map(all_region_ids,  self.region_contract)
        countries_map = self._fetch_map(all_country_ids, self.country_contract)

        # Set data
        for p in products:
            p.files = [
                self._to_dict(files_map[fid])
                for fid in (p.files_ids or [])
                if fid in files_map
            ]
            p.city    = self._to_dict(cities_map.get(p.city_id))
            p.region  = self._to_dict(regions_map.get(p.region_id))
            p.country = self._to_dict(countries_map.get(p.country_id))


    def get(self, id: int) -> ProductModel:
        result = super().get(id)

        if not result:
            return result

        self._attach_products([result])

        return result

    def get_all(self, user_id=None, page: int = 1, page_size: int = 20):
        qs = (
            self.model.objects.filter(owner_id=user_id)
            if user_id
            else self.model.objects.all()
        )

        paginator = Paginator(qs, page_size)
        page_products = list(paginator.page(page).object_list)

        if not page_products:
            return page_products

        self._attach_products(page_products)

        return page_products

    def create(self, user_id: int, data: dict) -> ProductModel:
        self.geo_validate(data)

        data["owner_id"] = user_id
        files = data.pop("files")
        file_list = self.file_contract.create_many(files, user_id)
        file_ids = [i.id for i in file_list]
        data["files_ids"] = file_ids
        result = super().create(data)
        self._attach_products([result])
        return result

    def update(self, id: int, user_id: int, data: dict) -> ProductModel:
        self.geo_validate(data)
        product = self.get(id)
        if int(user_id) == product.owner_id:
            with transaction.atomic():
                if "files" in data.keys():
                    files = data.pop("files")
                    target_ids = product.files_ids
                    self.file_contract.update_many(files, user_id, target_ids)
                result = super().update(id, data)
                self._attach_products([result])
                return result
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
            country = self.country_contract.get(data["country_id"])
            region = self.region_contract.get(
                data["region_id"]
            )
            city = self.city_contract.get(data["city_id"])
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
