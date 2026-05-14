from dataclasses import dataclass

@dataclass(frozen=True)
class AllProductsDTO:
    id: int
    title: str
    description: str
    price: int