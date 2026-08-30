from dataclasses import dataclass
from typing import Optional

from core.dto.geo.geo_dto import (
    CountryShortDTO,
    RegionShortDTO,
    CityShortDTO,
)

from apps.geo.contracts.dto.city_dto import CityDTO
from apps.geo.contracts.dto.country_dto import CountryDTO
from apps.geo.contracts.dto.region_dto import RegionDTO


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
    country_id: Optional[int]
    region_id: Optional[int]
    city_id: Optional[int]

@dataclass(frozen=True)
class LocationOutDTO:
    country: CountryDTO | None
    region: RegionDTO | None
    city: CityDTO | None

@dataclass(frozen=True)
class LocationStarOutDTO:
    country: CountryDTO
    region: RegionDTO
    city: CityDTO