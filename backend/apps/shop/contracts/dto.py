from dataclasses import dataclass
from datetime import datetime
from typing import BinaryIO

from apps.files.dto import FileDTO
from apps.geo.contracts.dto.city_dto import CityDTO
from apps.geo.contracts.dto.country_dto import CountryDTO
from apps.geo.contracts.dto.region_dto import RegionDTO
from apps.search.dto import CategoryDTO
from apps.shop.enums import ProductStatus
from apps.users.dto.user import UserDTO


@dataclass(frozen=True)
class ProductDTO:
    id: int
    owner: UserDTO
    title: str
    description: str
    created_at: datetime
    country: CountryDTO
    region: RegionDTO
    city: CityDTO
    category: CategoryDTO
    price: int
    visible: bool
    files: dict[int, FileDTO]
    status: ProductStatus = ProductStatus.NEW


@dataclass(frozen=True)
class ProductUpdateDTO:
    id: int
    title: str | None = None
    description: str | None = None
    country_id: int | None = None
    region_id: int | None = None
    city_id: int | None = None
    category_id: int | None = None
    price: int | None = None
    status: ProductStatus = ProductStatus.NEW
    update_files: dict[int, BinaryIO] | None = None
    create_files: list[BinaryIO] | None = None
    keep_files_ids: list[int] | None = None


@dataclass(frozen=True)
class ProductCreateDTO:
    title: str
    description: str
    country_id: int
    region_id: int
    city_id: int
    category_id: int
    price: int
    files: list[BinaryIO]
    status: ProductStatus = ProductStatus.NEW
