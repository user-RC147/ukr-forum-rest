from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class User_Id_OutDTO:
    id:int



@dataclass(frozen=True)
class UserOutDTO:
    id:int
    username:Optional[str]
    display_name:str