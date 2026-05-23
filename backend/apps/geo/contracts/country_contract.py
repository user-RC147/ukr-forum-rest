from apps.geo.services.geo_service import GeoService
from apps.geo.protocols.country import CountryContractProtocol
from apps.geo.dto.country import CountryDTO
from dataclasses import fields


class CountryContract:
    def __init__(self, service: GeoService | None = None) -> None:
        self.service = service or GeoService()
        self._dto_fields = {f.name for f in fields(CountryDTO)}

    def get_country(self, country_id: int) -> CountryDTO:
        data = self.service.get_country(country_id)

        return self._to_dto(data)

    def _to_dto(self, data) -> CountryDTO:
        return CountryDTO(**{field: getattr(data, field) for field in self._dto_fields})


def get_country_contract() -> CountryContractProtocol:
    return CountryContract()
