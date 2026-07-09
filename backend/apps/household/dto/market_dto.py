from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CountryDTO:
    id:int
    name:str
    name_ua:str
    code:str
    flag_emoji:str
    currency:str


@dataclass(frozen=True)
class RegionDTO:
    id:int
    name:str
    name_ua:str
    country_id:int

 
@dataclass(frozen=True)
class CityDTO:
    id:int
    name:str
    name_ua:str
    country_id:int
    region_id: int
    latitude:Decimal
    longitude:Decimal
    

@dataclass(frozen=True)
class MarketLocationDTO:
    country:'CountryDTO'
    region:'RegionDTO'
    city:'CityDTO'


@dataclass(frozen=True)
class ListMarketDTO:
    name:int
    

@dataclass(frozen=True)
class CreateMarketInDTO:
    name:str
    address_line: str
    country_id:int
    region_id:int
    city_id:int


@dataclass(frozen=True)
class MarketOutDTO:
    id:int
    name:str
    address_line: str
    country_id:int
    region_id:int
    city_id:int


@dataclass(frozen=True)
class MarketFullOutDTO:
    id:int
    name:str
    address_line: str
    location:'MarketLocationDTO'


