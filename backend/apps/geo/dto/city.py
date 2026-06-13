from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CityDTO:
    """
    Публічне представлення міста.
    """
    id: int
    name: str
    name_ua: str
    country_id: int
    region_id: int
    latitude: Decimal
    longitude: Decimal