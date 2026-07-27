from dataclasses import dataclass
from re import S


@dataclass(frozen=True)
class Category_Id_Name_OutDTO:
    id:int
    name:str

@dataclass(frozen=True)
class CategoryOutDTO:
    id:int
    name:str
    icon:str
    is_active:bool
    parent_id:int