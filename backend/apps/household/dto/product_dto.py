from dataclasses import dataclass
from typing import Optional
from .unit_of_measure_dto import UnitOfMeasureOutDTO


@dataclass(frozen=True)
class CategoryProductDTO:
    id:int
    name:str
    icon:str
    is_active:bool
    parent:Optional[int]


@dataclass(frozen=True)
class ProductOutDTO:
    id:int
    name:str
    unit_of_measure:UnitOfMeasureOutDTO
    created_by: int
    category:CategoryProductDTO



@dataclass(frozen=True)
class CreateProductInDTO:
    name:str
    unit_of_measure_id: int
    created_by_id: int
    category_id:Optional[int]=None
