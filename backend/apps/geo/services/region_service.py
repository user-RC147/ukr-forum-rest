from collections.abc import Iterable

from apps.geo.dto.region import RegionDTO
from apps.geo.ports.repos import RegionRepositoryPort
from apps.geo.repositories.region_repository import get_repo_region


class RegionService:
    def __init__(self, repo: RegionRepositoryPort | None = None) -> None:
        self.repo = repo if repo is not None else get_repo_region()

    def get(self, id: int) -> RegionDTO:
        return self.repo.get(id)

    def get_many(
        self,
        region_ids: Iterable[int],
    ) -> list[RegionDTO]:
        return self.repo.get_many(region_ids)

    def get_by_country(self, country_id: int):
        return self.repo.get_by_country(country_id)


def get_service_region() -> RegionService:
    return RegionService()
