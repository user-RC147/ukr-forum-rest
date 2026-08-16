from collections.abc import Iterable

from apps.geo.dto.country_dto import CountryDTO
from apps.geo.ports.repo_ports import CountryRepositoryPort
from apps.geo.repositories.country_repository import get_repo_country


class CountryService:
    def __init__(self, repo: CountryRepositoryPort | None = None) -> None:
        self.repo = repo if repo is not None else get_repo_country()

    def get(self, id: int) -> CountryDTO:
        return self.repo.get(id)

    def get_many(
        self,
        country_ids: Iterable[int] | None = None,
    ) -> list[CountryDTO]:
        return self.repo.get_many(country_ids)

    def search(self, query: str) -> list[CountryDTO]:
        return self.repo.search(query)


def get_service_country() -> CountryService:
    return CountryService()
