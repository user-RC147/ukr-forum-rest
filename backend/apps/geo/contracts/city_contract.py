from apps.geo.services.geo_service import GeoService
from apps.geo.protocols.city import CityContractProtocol
from apps.geo.dto.city import CityDTO
from dataclasses import fields


class CityContract:
    def __init__(self, service: GeoService | None = None) -> None:
        self.service = service or GeoService()
        self._dto_fields = {f.name for f in fields(CityDTO)}

    def get_city(self, city_id: int, region_id: int) -> CityDTO:
        data = self.service.get_city(city_id, region_id)

        return self._to_dto(data)

    def _to_dto(self, data) -> CityDTO:
        return CityDTO(**{field: getattr(data, field) for field in self._dto_fields})


def get_city_contract() -> CityContractProtocol:
    return CityContract()
