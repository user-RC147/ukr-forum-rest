import dataclasses
import logging

from django.core.paginator import Paginator
from django.db import transaction

from apps.files.contracts import get_file_contract
from apps.files.dto import FileUpdatePlan
from apps.geo.contracts.city_contract import get_city_contract
from apps.geo.contracts.country_contract import get_country_contract
from apps.geo.contracts.region_contract import get_region_contract
from apps.search.contracts.category_contract import get_category_contract

from .dto import ProductDTO, ProductCreateDTO, ProductUpdateDTO
from .exceptions import ProductPermissionError
from .repository import get_repo, ProductRepository

logger = logging.getLogger("shop")


class ProductService:
    def __init__(self, repo: ProductRepository | None = None) -> None:
        self.repo = repo or get_repo()
        self.country_contract = get_country_contract()
        self.region_contract = get_region_contract()
        self.city_contract = get_city_contract()
        self.file_contract = get_file_contract()
        self.category_contract = get_category_contract()

    def _fetch_map(self, ids: list[int | None], contract) -> dict:
        """Deduplicate ids and 1 batch-request via get_many"""
        unique_ids = {i for i in ids if i is not None}
        if not unique_ids:
            return {}
        return contract.get_many(list(unique_ids))

    @staticmethod
    def _to_dict(obj) -> dict | None:
        return dataclasses.asdict(obj) if obj is not None else None

    def _attach_products(self, products: list[dict]) -> None:
        if not products:
            return

        # (field with ids in product, contract, name field, is_many)
        relations = [
            ("country_id", self.country_contract, "country", False),
            ("region_id", self.region_contract, "region", False),
            ("city_id", self.city_contract, "city", False),
            ("category_id", self.category_contract, "category", False),
            ("file_ids", self.file_contract, "files", True),
        ]

        maps = {}
        for id_field, contract, result_field, is_many in relations:
            if is_many:
                ids = [i for p in products for i in (p[id_field] or [])]
            else:
                ids = [p[id_field] for p in products]
            maps[result_field] = self._fetch_map(ids, contract)

        for p in products:
            p["country"] = self._to_dict(maps["country"].get(p["country_id"]))
            p["region"] = self._to_dict(maps["region"].get(p["region_id"]))
            p["city"] = self._to_dict(maps["city"].get(p["city_id"]))
            p["category"] = self._to_dict(maps["category"].get(p["category_id"]))
            p["files"] = [
                self._to_dict(maps["files"][fid])
                for fid in (p["file_ids"] or [])
                if fid in maps["files"]
            ]

    def get(self, id:int) -> ProductDTO:
        result = dataclasses.asdict(self.repo.get(id))

        self._attach_products([result])

        return _to_dto(result)

    def get_all(self, user_id=None, page: int = 1, page_size: int = 20) -> list[ProductDTO]:

        result = self.repo.get_many(user_id)

        paginator = Paginator(result, page_size)
        page_products = list(paginator.page(page).object_list)

        if not page_products:
            return page_products

        result = [dataclasses.asdict(p) for p in page_products]

        self._attach_products(result)

        return [_to_dto(p) for p in result]

    def create(self, data: ProductCreateDTO) -> ProductDTO:
        # validate geo
        self.country_contract.get(data.country_id)
        self.region_contract.get(data.region_id)
        self.city_contract.get(data.city_id)

        files = data.files

        data: dict = dataclasses.asdict(
            dataclasses.replace(data, files=[])
        )

        file_list = self.file_contract.create_many(files, data["owner_id"])
        file_ids = [i.id for i in file_list]
        data["file_ids"] = file_ids
        data.pop("files")

        result = dataclasses.asdict(self.repo.create(data))
        self._attach_products([result])
        return _to_dto(result)

    def update(self, user_id: int, data: ProductUpdateDTO) -> ProductDTO:

        product = self.get(data.id)
        fields = {
            f.name: getattr(data, f.name)
            for f in dataclasses.fields(data)
            if f.name != "id" and getattr(data, f.name) is not None
        }

        update_files, create_files = fields.pop("update_files", None), fields.pop("create_files", None)
        update_file_ids, keep_files_ids = fields.pop("update_file_ids", None), fields.pop("keep_files_ids", None)

        if user_id == product.owner_id:
            with transaction.atomic():
                has_file_changes = any(
                    v is not None
                    for v in (
                        update_files,
                        create_files,
                        update_file_ids,
                        keep_files_ids,
                    )
                )

                if has_file_changes:
                    item_ids = list(product.files.keys())
                    plan = FileUpdatePlan(
                        keep_ids=keep_files_ids or [],
                        update_ids=update_file_ids or [],
                    )

                    update_files_map = dict(
                        zip(update_file_ids or [], update_files or [], strict=True)
                    )

                    updated_file_dtos = self.file_contract.update_many(
                        user_id=user_id,
                        item_ids=item_ids,
                        plan=plan,
                        update_files=update_files_map,
                        create_files=create_files,
                    )

                    fields["file_ids"] = [f.id for f in updated_file_dtos]

                product_id = data.id
                result = dataclasses.asdict(self.repo.update(product_id, fields))
                self._attach_products([result])
                return _to_dto(result)
        else:
            logger.warning(
                "Access denied to product id: %s with user_id: %s", product.id, fields["owner_id"]
            )
            raise ProductPermissionError

    def delete(self, id: int, user_id: int) -> None:

        product = self.get(id)
        if int(user_id) == product.owner_id:
            with transaction.atomic():
                if product.files:
                    self.file_contract.delete_many(list(product.files.keys()))
                result = self.repo.delete(id)
        else:
            logger.warning(
                "Access denied to product id: %s with user_id: %s", product.id, user_id
            )
            raise ProductPermissionError

        return result

    def nullify_geo(self, field_name: str, geo_id: int) -> int:

        return self.repo.nullify_geo(field_name, geo_id)

    def delete_all_by_user(self, user_id: int) -> int:
        return self.repo.delete_by_user(user_id)


def _to_dto(data) -> ProductDTO:
    return ProductDTO(
        id=data["id"],
        owner_id=data["owner_id"],
        title=data["title"],
        description=data["description"],
        created_at=data["created_at"],
        country=data["country"],
        region=data["region"],
        city=data["city"],
        category=data["category"],
        price=data["price"],
        visible=data["visible"],
        files=data["files"],
    )



def get_service() -> ProductService:
    return ProductService()
