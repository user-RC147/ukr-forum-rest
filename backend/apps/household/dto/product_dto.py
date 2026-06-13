from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateProductInDTO:
    name:str
    unit_of_measure: str
    category_id:Optional[int]=None