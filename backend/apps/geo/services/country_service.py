from collections.abc import Iterable

from apps.geo.dto.country import CountryDTO
from apps.geo.repositories.country_repository import CountryRepository


class CountryService:
    def __init__(self, model=CountryRepository()) -> None:
        self.model = model

    def get(self, id: int) -> CountryDTO:
        return self.model.get(id)

    def get_many(
        self,
        country_ids: Iterable[int] | None = None,
    ) -> list[CountryDTO]:
        return self.model.get_many(country_ids)

    def search(self, query: str) -> list[CountryDTO]:
        return self.model.search(query)
