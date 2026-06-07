from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProductDTO:
    id: int
    title: str
    description: str
    price: int
    visible: Optional[bool]
