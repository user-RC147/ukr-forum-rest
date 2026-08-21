from dataclasses import dataclass

from core.dto.geo.geo_dto import (
    CountryShortDTO,
    RegionShortDTO,
    CityShortDTO,
)

from apps.geo.dto.country import CountryDTO
from apps.geo.dto.region import RegionDTO
from apps.geo.dto.city import CityDTO


@dataclass(frozen=True)
class LocationShortOutDTO:
    country: CountryShortDTO
    region: RegionShortDTO
    city: CityShortDTO


@dataclass(frozen=True)
class Location_Id_InDTO:
    country_id: int
    region_id: int
    city_id: int

@dataclass(frozen=True)
class Location_Id_OutDTO:
    country_id: int
    region_id: int
    city_id: int


@dataclass(frozen=True)
class LocationOutDTO:
    country: CountryDTO
    region: RegionDTO
    city: CityDTO
