from dataclasses import dataclass


@dataclass
class RegionDTO:
    id: int
    name: str
    name_ua: str
    country_id: int
