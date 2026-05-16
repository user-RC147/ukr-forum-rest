from dataclasses import dataclass


@dataclass(frozen=True)
class ProductDTO:
    id: int
    title: str
    description: str
    price: int
