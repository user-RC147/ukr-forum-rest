from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class CityDTO:
    """
    Публічне представлення міста.
    """
    id: int
    name: str
    name_ua: str
    country_id: int
    region: dict
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None