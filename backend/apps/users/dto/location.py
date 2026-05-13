from dataclasses import dataclass
from typing import Optional

@dataclass
class LocationUpdateDTO:
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    city_id: Optional[int] = None