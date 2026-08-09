from apps.geo.dto.city import CityDTO
from apps.geo.protocols.city import CityContractProtocol
from apps.geo.services.city_service import CityService


class CityContract:
    def __init__(self, service=CityService()) -> None:
        self.service = service

    def get(self, city_id: int) -> CityDTO:
        return self.service.get(city_id)

    def get_many(self, city_ids: list[int]) -> dict[int, CityDTO]:
        data = self.service.get_many(city_ids)
        data = {d.id: d for d in data}
        return data

    def get_by_region(self, region_id: int) -> dict[int, CityDTO]:
        data = self.service.get_by_region(region_id)
        data = {d.id: d for d in data}
        return data


def get_city_contract() -> CityContractProtocol:
    return CityContract()
