from typing import Protocol

from apps.geo.dto.country_dto import CountryDTO


class CountryContractProtocol(Protocol):
    def get(self, country_id: int) -> CountryDTO: ...
    def get_many(self, country_ids: list[int] | None) -> dict[int, CountryDTO]: ...
