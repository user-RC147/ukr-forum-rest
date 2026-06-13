from dataclasses import dataclass

@dataclass
class RegionDTO:
    """
    Публічне представлення регіону.
    """
    id: int
    name: str
    name_ua: str
    country_id: int