from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ProductDTO:
    id: int
    owner_id: int
    title: str
    description: str
    created_at: datetime
    country_id: int
    price: int
    visible: bool | None
    files: list | None
