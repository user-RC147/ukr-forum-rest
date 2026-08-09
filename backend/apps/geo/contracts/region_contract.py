from apps.geo.dto.region import RegionDTO
from apps.geo.protocols.region import RegionContractProtocol
from apps.geo.services.region_service import RegionService


class RegionContract:
    def __init__(self, service=RegionService()) -> None:
        self.service = service

    def get(self, region_id: int) -> RegionDTO:
        return self.service.get(region_id)

    def get_many(self, region_ids: list[int]) -> dict[int, RegionDTO]:
        data = self.service.get_many(region_ids)
        data = {d.id: d for d in data}
        return data

    def get_by_country(self, country_id: int) -> dict[int, RegionDTO]:
        data = self.service.get_by_region(country_id)
        data = {d.id: d for d in data}
        return data


def get_region_contract() -> RegionContractProtocol:
    return RegionContract()
