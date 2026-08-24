from dataclasses import dataclass
from decimal import Decimal

from core.dto.geo.location_dto import LocationOutDTO,Location_Id_InDTO,Location_Id_OutDTO,LocationShortOutDTO
from core.dto.geo.geo_dto import CountryShortDTO,RegionShortDTO,CityShortDTO
from apps.geo.contracts.country_contract import CountryDTO
from apps.geo.contracts.region_contract import RegionDTO
from apps.geo.contracts.dto.city_dto import CityDTO,City_id_region_DTO

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



