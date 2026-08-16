from apps.geo.dto.country_dto import CountryDTO
from apps.geo.protocols.country_protocol import CountryContractProtocol
from apps.geo.services.country_service import CountryService


class CountryContract:
    def __init__(self, service=CountryService()) -> None:
        self.service = service

    def get(self, country_id: int) -> CountryDTO:
        return self.service.get(country_id)

    def get_many(self, country_ids: list[int] | None) -> dict[int, CountryDTO]:
        data = self.service.get_many(country_ids)
        data = {d.id: d for d in data}
        return data


def get_country_contract() -> CountryContractProtocol:
    return CountryContract()
