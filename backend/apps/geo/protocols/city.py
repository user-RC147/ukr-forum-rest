from typing import Protocol

from apps.geo.dto.city import CityDTO


class CityContractProtocol(Protocol):
    def get(self, city_id: int) -> CityDTO: ...
    def get_many(self, cities_ids: list[int]) -> dict[int, CityDTO]: ...
