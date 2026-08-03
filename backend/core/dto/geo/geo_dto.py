from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CountryShortDTO:
    """
    DTO для передачі даних про країну між модулями.
    frozen=True робить об'єкт незмінним (read-only), що гарантує безпеку даних.
    """
    id:int
    name:str
    name_ua: str  # ← Додано для підтримки української мови
    code: str     # ← Додано ISO-код країни (наприклад, 'UA'), знадобиться для API


@dataclass(frozen=True)
class RegionShortDTO:
    """
    DTO для передачі даних про регіону між модулями.
    frozen=True робить об'єкт незмінним (read-only), що гарантує безпеку даних.
    """
    id:int
    name:str
    name_ua: str  # ← Додано для підтримки української мови
    country_id: int  # ← Додано зв'язок з країною


@dataclass(frozen=True)
class CityShortDTO:
    """
    DTO для передачі даних про місто між модулями.
    frozen=True робить об'єкт незмінним (read-only), що гарантує безпеку даних.
    """
    id:int
    name:str
    name_ua:str
    region_id:int

#===================================

@dataclass(frozen=True)
class CountryOutDTO:
    id:int
    name:str
    name_ua:str
    code:str
    flag_emoji:str
    currency:str

@dataclass(frozen=True)
class RegionOutDTO:
    id:int
    name:str
    name_ua:str
    country_id:int

@dataclass(frozen=True)
class CityOutDTO:
    id:int
    name:int
    name_ua:str
    country_id:int
    region_id:int
    latitude:Decimal
    longitude:Decimal


#================================================
