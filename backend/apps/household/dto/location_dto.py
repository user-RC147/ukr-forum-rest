from dataclasses import dataclass
from decimal import Decimal

from apps.geo.contracts.dto import country_dto


@dataclass(frozen=True)
class CountryOutDTO:
    id:int
    name:str
    name_ua:str
    code:str
    flag_emoji:str
    currency:str

@dataclass(frozen=True)
class RegionOutDTO:
    id:int
    name:str
    name_ua:str
    country_id:int

@dataclass(frozen=True)
class CityOutDTO:
    id:int
    name:int
    name_ua:str
    country_id:int
    region_id:int
    latitude:Decimal
    longitude:Decimal



@dataclass(frozen=True)
class CountryNameOutDTO:
    id:int
    name:str
    code:str

@dataclass(frozen=True)
class RegionNameOutDTO:
    id:int
    name:str
    name_ua:str

@dataclass(frozen=True)
class CityNameOutDTO:
    id:int
    name:int
    name_ua:str

@dataclass(frozen=True)
class LocationId_Name_OutDTO:
    country:CountryNameOutDTO
    region:RegionNameOutDTO
    city:CityNameOutDTO



@dataclass(frozen=True)
class LocationIdInDTO:
    country_id:int
    region_id:int
    city_id:int

@dataclass(frozen=True)
class LocationIdOutDTO:
    country_id:int
    region_id:int
    city_id:int


@dataclass(frozen=True)
class LocationOutDTO:
    country:CountryOutDTO
    region:RegionOutDTO
    city:CityOutDTO