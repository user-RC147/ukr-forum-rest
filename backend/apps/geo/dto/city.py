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
    region: dict
    latitude: Decimal | None = None
    longitude: Decimal | None = None
