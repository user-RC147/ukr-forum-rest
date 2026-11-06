from dataclasses import dataclass
from decimal import Decimal

from apps.geo.contracts.country_contract import CountryDTO
from apps.geo.contracts.dto.city_dto import City_id_region_DTO, CityDTO
from apps.geo.contracts.region_contract import RegionDTO
from core.dto.geo.geo_dto import CityShortDTO, CountryShortDTO, RegionShortDTO
from core.dto.geo.location_dto import (
    Location_Id_InDTO,
    Location_Id_OutDTO,
    LocationOutDTO,
    LocationShortOutDTO,
)


@dataclass(frozen=True)
class CountryNameOutDTO:
    id: int
    name: str
    code: str


@dataclass(frozen=True)
class RegionNameOutDTO:
    id: int
    name: str
    name_ua: str


@dataclass(frozen=True)
class CityNameOutDTO:
    id: int
    name: int
    name_ua: str


@dataclass(frozen=True)
class LocationId_Name_OutDTO:
    country: CountryNameOutDTO
    region: RegionNameOutDTO
    city: CityNameOutDTO
