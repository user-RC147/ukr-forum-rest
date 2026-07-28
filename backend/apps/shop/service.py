import dataclasses
import logging

from django.db import transaction

from apps.files.contracts import get_file_contract
from apps.files.dto import FileUpdatePlan
from apps.geo.contracts.city_contract import get_city_contract
from apps.geo.contracts.country_contract import get_country_contract
from apps.geo.contracts.region_contract import get_region_contract
from apps.search.contracts.category_contract import get_category_contract
from apps.users.contracts.user_contract import get_user_contract

from .dto import ProductCreateDTO, ProductDTO, ProductUpdateDTO, RequestUserDTO, PageDTO
from backend.core.paginator.paginator import paginate_build
from backend.core.paginator.dto import PaginatorDTO
from .exceptions import ProductPermissionError
from .repository import ProductRepository, get_repo

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, repo: ProductRepository | None = None) -> None:
        self.repo = repo or get_repo()
        self.country_contract = get_country_contract()
        self.region_contract = get_region_contract()
        self.city_contract = get_city_contract()
        self.file_contract = get_file_contract()
        self.category_contract = get_category_contract()
        self.user_contract = get_user_contract()

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
            ("owner_id", self.user_contract, "owner", False),
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
            p["owner"] = self._to_dict(maps["owner"].get(p["owner_id"]))
            p["files"] = [
                self._to_dict(maps["files"][fid])
                for fid in (p["file_ids"] or [])
                if fid in maps["files"]
            ]

    def get(self, id: int) -> ProductDTO:
        result = dataclasses.asdict(self.repo.get(id))

        self._attach_products([result])

        return _to_dto_product(result)

    def get_many(
        self,
        product_ids: list[int],
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatorDTO[ProductDTO]:
        if not product_ids:
            return paginate_build([], 0, page, page_size)

        qs = self.repo.get_many(
            product_ids=product_ids, page=page, page_size=page_size
        )
        if not qs.items:
            return paginate_build([], 0, page, page_size)

        result = [dataclasses.asdict(p) for p in qs.items]

        self._attach_products(result)

        result = [_to_dto_product(p) for p in result]
        return paginate_build(result, qs.count, page, page_size)

    def get_all(
        self,
        page: int = 1,
        user: RequestUserDTO | None = None,
        user_id: int | None = None,
        page_size: int = 20,
    ) -> PaginatorDTO[ProductDTO]:

        if user_id:
            ProductAccessPolicy.can_view_as_owner(user, user_id)

        qs = self.repo.get_many(page=page, page_size=page_size, user_id=user_id)
        if not qs.items:
            return paginate_build([], qs.count, page, page_size)

        result = [dataclasses.asdict(p) for p in qs.items]

        self._attach_products(result)

        result = [_to_dto_product(p) for p in result]
        return paginate_build(result, qs.count, page, page_size)

    def create(self, user: RequestUserDTO, data: ProductCreateDTO) -> ProductDTO:
        # validate geo
        self.country_contract.get(data.country_id)
        self.region_contract.get(data.region_id)
        self.city_contract.get(data.city_id)

        files = data.files

        data: dict = dataclasses.asdict(dataclasses.replace(data, files=[]))
        data["owner_id"] = user.id
        file_list = self.file_contract.create_many(files, data["owner_id"])
        file_ids = [i.id for i in file_list]
        data["file_ids"] = file_ids
        data.pop("files")

        product = self.repo.create(data)

        result = dataclasses.asdict(product)
        self._attach_products([result])

        dto = _to_dto_product(result)

        logger.info(
            "Product was created",
            extra={"product_id": product.id, "event": "create_product"},
        )

        return dto

    def update(self, user: RequestUserDTO, data: ProductUpdateDTO) -> ProductDTO:

        product = self.get(data.id)
        ProductAccessPolicy.can_edit(user, product)
        fields = {
            f.name: getattr(data, f.name)
            for f in dataclasses.fields(data)
            if f.name != "id" and getattr(data, f.name) is not None
        }

        update_files = fields.pop("update_files", None)
        create_files = fields.pop("create_files", None)
        keep_files_ids = fields.pop("keep_files_ids", None)

        with transaction.atomic():
            has_file_changes = any(
                v is not None
                for v in (
                    update_files,
                    create_files,
                    keep_files_ids,
                )
            )

            if has_file_changes:
                item_ids = [p["id"] for p in product.files]
                plan = FileUpdatePlan(
                    keep_ids=keep_files_ids or [],
                    update_ids=list(update_files.keys()) or [],
                )

                updated_file_dtos = self.file_contract.update_many(
                    user_id=user.id,
                    item_ids=item_ids,
                    plan=plan,
                    update_files=update_files,
                    create_files=create_files,
                )

                fields["file_ids"] = [f.id for f in updated_file_dtos]

            product_id = data.id
            result = dataclasses.asdict(self.repo.update(product_id, fields))
            self._attach_products([result])
            result = _to_dto_product(result)

            logger.info(
                "Product was updated",
                extra={"product_id": product_id, "event": "update_product"},
            )

            return result

    def delete(self, user: RequestUserDTO, id: int) -> None:

        product = self.get(id)

        ProductAccessPolicy.can_edit(user, product)

        with transaction.atomic():
            if product.files:
                self.file_contract.delete_many([p["id"] for p in product.files])
            result = self.repo.delete(id)

        logger.info(
            "Deleted product",
            extra={"product_id": product.id, "event": "delete_product"},
        )

        return result

    def nullify_geo(self, field_name: str, geo_id: int) -> int:

        return self.repo.nullify_geo(field_name, geo_id)

    def delete_all_by_user(self, user_id: int) -> int:
        return self.repo.delete_by_user(user_id)


def _to_dto_product(data) -> ProductDTO:
    return ProductDTO(
        id=data["id"],
        owner=data["owner"],
        title=data["title"],
        description=data["description"],
        created_at=data["created_at"],
        country=data["country"],
        region=data["region"],
        city=data["city"],
        category=data["category"],
        status=data["status"],
        price=data["price"],
        visible=data["visible"],
        files=data["files"],
    )

def _to_dto_page(data: list[ProductDTO], total: int):
    return PageDTO(items=data, total=total)


def get_service() -> ProductService:
    return ProductService()


class ProductAccessPolicy:
    @staticmethod
    def can_view_as_owner(
        user: RequestUserDTO, owner_id: int, add_extra: dict | None = None
    ) -> None:

        if user.id != owner_id and not user.is_staff:
            extra = {
                "user_id from request": user.id,
                "owner_id": owner_id,
                "event": "product_validation",
            }
            if add_extra:
                extra.update(add_extra)
            raise ProductPermissionError(extra=extra)

    @staticmethod
    def can_edit(user: RequestUserDTO, product: ProductDTO) -> None:
        ProductAccessPolicy.can_view_as_owner(
            user, product.owner["id"], add_extra={"item_id": product.id}
        )
