from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CountryDTO:
    """
    DTO для передачі даних про країну між модулями.
    frozen=True робить об'єкт незмінним (read-only), що гарантує безпеку даних.
    """
    id:int
    name:str
    name_ua: str  # ← Додано для підтримки української мови
    code: str     # ← Додано ISO-код країни (наприклад, 'UA'), знадобиться для API


@dataclass(frozen=True)
class RegionDTO:
    """
    DTO для передачі даних про регіону між модулями.
    frozen=True робить об'єкт незмінним (read-only), що гарантує безпеку даних.
    """
    id:int
    name:str
    name_ua: str  # ← Додано для підтримки української мови
    country_id: int  # ← Додано зв'язок з країною


@dataclass(frozen=True)
class CityDTO:
    """
    DTO для передачі даних про місто між модулями.
    frozen=True робить об'єкт незмінним (read-only), що гарантує безпеку даних.
    """
    id:int
    name:str
    name_ua:str
    region_id:int