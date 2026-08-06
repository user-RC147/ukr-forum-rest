from collections.abc import Iterable

from apps.geo.dto.city import CityDTO
from apps.geo.repositories.city_repository import CityRepository


class CityService:
    def __init__(self, model=CityRepository()) -> None:
        self.model = model

    def get(self, id: int) -> CityDTO:
        return self.model.get(id)

    def get_many(
        self,
        city_ids: Iterable[int],
    ) -> list[CityDTO]:
        return self.model.get_many(city_ids)

    def get_by_region(self, region_id: int):
        return self.model.get_by_region(region_id)

    def search(self, query: str, country_id: int) -> list[CityDTO]:
        return self.model.search(query, country_id)
