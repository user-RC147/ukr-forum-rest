from collections.abc import Iterable
from typing import Protocol

from apps.geo.contracts.dto.city_dto import CityDTO
from apps.geo.contracts.dto.country_dto import CountryDTO
from apps.geo.contracts.dto.region_dto import RegionDTO


class CityRepositoryPort(Protocol):
    def get(self, city_id: int) -> CityDTO: ...

    def get_many(
        self,
        city_ids: Iterable[int],
    ) -> list[CityDTO]: ...

    def get_by_region(self, region_id: int) -> list[CityDTO]: ...
    def search(self, query: str, country_id: int) -> list[CityDTO]: ...


class RegionRepositoryPort(Protocol):
    def get(self, region_id: int) -> RegionDTO: ...

    def get_many(
        self,
        region_ids: Iterable[int],
    ) -> list[RegionDTO]: ...

    def get_by_country(self, country_id: int) -> list[RegionDTO]: ...


class CountryRepositoryPort(Protocol):
    def get(self, country_id: int) -> CountryDTO: ...

    def get_many(
        self, country_ids: Iterable[int] | None = None
    ) -> list[CountryDTO]: ...

    def search(self, query: str) -> list[CountryDTO]: ...
