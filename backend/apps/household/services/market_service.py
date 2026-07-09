from multiprocessing import Value
from typing import Any
from requests import get
from apps.geo.api.views import regions
from apps.household.dto.market_dto import (
    CreateMarketInDTO,
    MarketFullOutDTO,
    MarketLocationDTO,
    MarketOutDTO,
    CountryDTO,
    RegionDTO,
    CityDTO,
)
from apps.household.models import market
from apps.household.repositories.maket_repo import MarketRepo
from apps.household.selectors.market_select import MarketSelector
from apps.geo.contracts.country_contract import get_country_contract
from apps.geo.contracts.region_contract import get_region_contract
from apps.geo.contracts.city_contract import get_city_contract


class MarketService:
    """
    Бізнес-логіка для роботи з магазинами (Markets).
    Реалізує гнучку перевірку гео-локації через зовнішній контракт модулів.
    """

    def __init__(self) -> None:
        self._selector = MarketSelector()
        self._repository = MarketRepo()
        self._country_contract = get_country_contract()
        self._region_contract = get_region_contract()
        self._city_contract = get_city_contract()

    # вибирає всі id з обєкту країн,регіонів,міст і створює set

    def get_locations_full_market(self,markets)->list[MarketFullOutDTO]:

        country_ids = set()
        region_ids = set()
        city_ids = set()    

        for item in markets:
            country_ids.add(item.country_id)
            region_ids.add(item.region_id)
            city_ids.add(item.city_id)

        countries = self._country_contract.get_many(country_ids)
        regions = self._region_contract.get_many(region_ids)
        cities = self._city_contract.get_many(city_ids)

        dto_markets = [
            MarketFullOutDTO(
                id=market.id,
                name=market.name,
                address_line=market.address_line,
                location=MarketLocationDTO(
                    country=CountryDTO(
                        id=countries[market.country_id].id,
                        name=countries[market.country_id].name,
                        name_ua=countries[market.country_id].name_ua,
                        code=countries[market.country_id].code,
                        flag_emoji=countries[market.country_id].flag_emoji,
                        currency=countries[market.country_id].currency,
                    ),
                    region=RegionDTO(
                        id=regions[market.region_id].id,
                        name=regions[market.region_id].name,
                        name_ua=regions[market.region_id].name_ua,
                        country_id=regions[market.region_id].country_id
                    ),
                    city=CityDTO(
                        id=cities[market.city_id].id,
                        name=cities[market.city_id].name,
                        name_ua=cities[market.city_id].name_ua,
                        country_id=cities[market.city_id].country_id,
                        region_id=cities[market.city_id].region['id'],
                        latitude=cities[market.city_id].latitude,
                        longitude=cities[market.city_id].longitude
                    ),
                ),
            )
            for market in markets
        ]        

        return dto_markets


    def location_market_exists(self,dto)->bool:
        self._country_contract.get(dto.country_id)
        self._region_contract.get(dto.region_id)
        self._city_contract.get(dto.city_id)
        
    def get_all(self):
        markets = self._selector.get_all()
        dto_markets = self.get_locations_full_market(markets)

        return dto_markets

    def create(self,dto:CreateMarketInDTO,user:int)->market:        

        try:
            self.location_market_exists(dto)
            return self._repository.create(dto,user)
        except Exception:
            raise Exception