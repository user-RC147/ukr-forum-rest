from typing import Protocol
from apps.geo.dto.region import RegionDTO

class RegionContractProtocol(Protocol):

    def get_region(self, region_id: int, country_id: int) -> RegionDTO: ...
    def get_many(self, regions_ids: list[int]) -> dict[int, RegionDTO]: ...