from dataclasses import dataclass
from datetime import datetime

from django.core.files.uploadedfile import UploadedFile

from apps.geo.dto.city import CityDTO
from apps.geo.dto.country import CountryDTO
from apps.geo.dto.region import RegionDTO
from apps.search.dto import CategoryDTO

from .enums import ProductStatus


@dataclass(frozen=True)
class RequestUserDTO:
    id: int
    is_staff: bool


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
    update_files: dict[int, UploadedFile] | None = None
    create_files: list[UploadedFile] | None = None
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
    files: list[UploadedFile]
    status: ProductStatus = ProductStatus.NEW


@dataclass(frozen=True)
class ProductRepoDTO:
    id: int
    owner_id: int
    title: str
    description: str
    created_at: datetime
    country_id: int
    region_id: int
    city_id: int
    category_id: int
    price: int
    visible: bool
    file_ids: list[int]
    status: ProductStatus = ProductStatus.NEW


@dataclass(frozen=True)
class ProductDTO:
    id: int
    owner_id: int
    title: str
    description: str
    created_at: datetime
    country: CountryDTO
    region: RegionDTO
    city: CityDTO
    category: CategoryDTO
    price: int
    visible: bool
    files: list[dict]
    status: ProductStatus = ProductStatus.NEW
