# apps/geo/dto/geo_dto.py
from dataclasses import dataclass


@dataclass
class CountryDTO:
    """
    Публічне представлення країни.
    Використовується іншими модулями — household, users тощо.
    """
    id: int
    name: str
    name_ua: str
    code: str
    flag_emoji: str


@dataclass
class RegionDTO:
    """
    Публічне представлення регіону.
    """
    id: int
    name: str
    name_ua: str


@dataclass
class CityDTO:
    """
    Публічне представлення міста.
    """
    id: int
    name: str
    name_ua: str