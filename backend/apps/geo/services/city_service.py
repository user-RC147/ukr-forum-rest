from collections.abc import Iterable

from apps.geo.dto.city import CityDTO
from apps.geo.ports.repos import CityRepositoryPort
from apps.geo.repositories.city_repository import get_repo_city


class CityService:
    def __init__(self, repo: CityRepositoryPort | None = None) -> None:
        self.repo = repo if repo is not None else get_repo_city()

    def get(self, id: int) -> CityDTO:
        return self.repo.get(id)

    def get_many(
        self,
        city_ids: Iterable[int],
    ) -> list[CityDTO]:
        return self.repo.get_many(city_ids)

    def get_by_region(self, region_id: int):
        return self.repo.get_by_region(region_id)

    def search(self, query: str, country_id: int) -> list[CityDTO]:
        return self.repo.search(query, country_id)


def get_service_city() -> CityService:
    return CityService()
