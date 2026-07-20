from dataclasses import dataclass



@dataclass(frozen=True)
class RoleOutDTO:
    id:int
    name:str
    name_ua:str
    is_bool:bool