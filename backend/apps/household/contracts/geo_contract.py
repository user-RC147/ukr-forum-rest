from typing import Protocol
from dataclasses import dataclass


@dataclass
class CountryData:
    id:int
    name:str
    code:str


@dataclass
class RegionData:
    id:int
    name:str
    country_id:int


@dataclass
class CityData:
    id:int
    name:str
    region_id:int





class IGeoContract(Protocol):

    def get_country(self,country_id:int) -> CountryData: ...

    def get_region(self, region_id:int) -> RegionData: ...

    def get_citie(self,city_id:int)->CityData: ...



class LocationProtocol(Protocol):
    """
    Контракт для моделей які мають локацію.
    Замість ForeignKey до geo моделей — просто id.
    """

    country_id: int | None
    region_id: int | None
    city_id: int | None
