from dataclasses import dataclass
from typing import Optional

from apps.geo.contracts.dto.city_dto import CityDTO
from apps.geo.contracts.dto.country_dto import CountryDTO
from apps.geo.contracts.dto.region_dto import RegionDTO
from core.dto.geo.geo_dto import (
    CityShortDTO,
    CountryShortDTO,
    RegionShortDTO,
)


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
    country_id: int | None
    region_id: int | None
    city_id: int | None


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
