from dataclasses import dataclass

from core.dto.geo.geo_dto import (
    CountryShortDTO,
    RegionShortDTO,
    CityShortDTO,
    CountryOutDTO,
    RegionOutDTO,
    CityOutDTO,
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
    country_id: int
    region_id: int
    city_id: int


@dataclass(frozen=True)
class LocationOutDTO:
    country: CountryOutDTO
    region: RegionOutDTO
    city: CityOutDTO
