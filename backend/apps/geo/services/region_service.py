from collections.abc import Iterable

from apps.geo.dto.region import RegionDTO
from apps.geo.repositories.region_repository import RegionRepository


class RegionService:
    def __init__(self, model=RegionRepository()) -> None:
        self.model = model

    def get(self, id: int) -> RegionDTO:
        return self.model.get(id)

    def get_many(
        self,
        region_ids: Iterable[int],
    ) -> list[RegionDTO]:
        return self.model.get_many(region_ids)

    def get_by_country(self, country_id: int):
        return self.model.get_by_country(country_id)
