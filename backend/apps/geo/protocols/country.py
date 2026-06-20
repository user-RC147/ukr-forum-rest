from typing import Protocol
from apps.geo.dto.country import CountryDTO

class CountryContractProtocol(Protocol):

    def get(self, country_id: int) -> CountryDTO: ...
    def get_many(self, countries_ids: list[int]) -> dict[int, CountryDTO]: ...