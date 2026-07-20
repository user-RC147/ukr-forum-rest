from dataclasses import dataclass
from decimal import Decimal

from apps.household.dto.location_dto import LocationId_Name_OutDTO, LocationIdInDTO, LocationOutDTO



@dataclass(frozen=True)
class ListMarketDTO:
    name:int
    

@dataclass(frozen=True)
class CreateMarketInDTO:
    name:str
    address_line: str
    location:LocationIdInDTO


@dataclass(frozen=True)
class Market_Id_Name_OutDTO:
    id:int
    name:str
    address_line: str
    location:LocationId_Name_OutDTO

@dataclass(frozen=True)
class Market_Id_OutDTO:
    id:int
    name:str
    address_line: str
    location:LocationIdInDTO

@dataclass(frozen=True)
class MarketFullOutDTO:
    id:int
    name:str
    address_line: str
    location:LocationOutDTO


