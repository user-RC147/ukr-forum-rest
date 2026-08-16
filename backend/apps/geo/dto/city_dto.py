from dataclasses import dataclass
from decimal import Decimal

from .region_dto import RegionDTO


@dataclass
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
