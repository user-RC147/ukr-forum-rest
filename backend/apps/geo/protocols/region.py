from typing import Protocol
from apps.geo.dto.region import RegionDTO

class RegionContractProtocol(Protocol):

    def get(self, region_id: int) -> RegionDTO: ...
    def get_many(self, regions_ids: list[int]) -> dict[int, RegionDTO]: ...