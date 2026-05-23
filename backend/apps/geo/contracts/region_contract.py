from apps.geo.services.geo_service import GeoService
from apps.geo.protocols.region import RegionContractProtocol
from apps.geo.dto.region import RegionDTO
from dataclasses import fields


class RegionContract:
    def __init__(self, service: GeoService | None = None) -> None:
        self.service = service or GeoService()
        self._dto_fields = {f.name for f in fields(RegionDTO)}

    def get_region(self, region_id: int, country_id: int) -> RegionDTO:
        data = self.service.get_region(region_id, country_id)

        return self._to_dto(data)

    def _to_dto(self, data) -> RegionDTO:
        return RegionDTO(**{field: getattr(data, field) for field in self._dto_fields})


def get_region_contract() -> RegionContractProtocol:
    return RegionContract()
