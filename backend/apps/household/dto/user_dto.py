from dataclasses import dataclass

@dataclass(frozen=True)
class User_Id_OutDTO:
    id:int



@dataclass(frozen=True)
class UserOutDTO:
    id:int
    username:str
    display_name:str