from typing import Protocol
from apps.geo.dto.city import CityDTO

class CityContractProtocol(Protocol):

    def get_city(self, city_id: int, region_id: int) -> CityDTO: ...