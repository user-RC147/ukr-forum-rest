from typing import Protocol
from apps.geo.dto.country import CountryDTO

class CountryContractProtocol(Protocol):

    def get_country(self, country_id: int) -> CountryDTO: ...