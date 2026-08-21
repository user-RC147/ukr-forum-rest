from dataclasses import dataclass
from datetime import datetime

from .enums import ProductStatus


@dataclass(frozen=True)
class RequestUserDTO:
    id: int
    is_staff: bool


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
