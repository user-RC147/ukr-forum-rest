from dataclasses import dataclass
from decimal import Decimal

from .region import RegionDTO


@dataclass(frozen=True)
class CityDTO:
    """
    Публічне представлення міста.
    """

    id: int
    name: str
    name_ua: str
    country_id: int
    region: RegionDTO
    latitude: Decimal | None = None
    longitude: Decimal | None = None


@dataclass(frozen=True)
class City_id_region_DTO:
    """
    Публічне представлення міста.
    """

    id: int
    name: str
    name_ua: str
    country_id: int
    region_id: int
    latitude: Decimal | None = None
    longitude: Decimal | None = None
