from multiprocessing import Value
from typing import Any
from requests import get
from apps.geo.api.views import regions
from apps.household.dto.market_dto import CreateMarketInDTO, MarketFullOutDTO,Market_Id_OutDTO
from apps.household.models import market
from apps.household.repositories.maket_repo import MarketRepo
from apps.household.selectors.market_select import MarketSelector
from apps.geo.contracts.country_contract import get_country_contract
from apps.geo.contracts.region_contract import get_region_contract
from apps.geo.contracts.city_contract import get_city_contract

from apps.household.dto.location_dto import (
    LocationOutDTO,
    CountryOutDTO,
    RegionOutDTO,
    CityOutDTO,
)


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

    def get_locations_full_market(self, markets:list[Market_Id_OutDTO]) -> list[MarketFullOutDTO]:

        country_ids = set()
        region_ids = set()
        city_ids = set()

        for item in markets:
            country_ids.add(item.location.country_id)
            region_ids.add(item.location.region_id)
            city_ids.add(item.location.city_id)

        countries = self._country_contract.get_many(country_ids)
        regions = self._region_contract.get_many(region_ids)
        cities = self._city_contract.get_many(city_ids)

        locations = {"countries": countries, "regions": regions, "cities": cities}

        return [_to_market_out(item, locations=locations)for item in markets]

    def location_market_exists(self, dto) -> bool:
        self._country_contract.get(dto.country_id)
        self._region_contract.get(dto.region_id)
        self._city_contract.get(dto.city_id)

    def get_all(self):
        markets = self._selector.get_all()
        dto_markets = self.get_locations_full_market(markets)



        return dto_markets

    def create(self, dto: CreateMarketInDTO, user: int) -> market:

        try:
            #self.location_market_exists(dto)
            return self._repository.create(dto, user)
        except Exception:
            raise Exception


# ==================================================================
def _to_location_country(data, countrys_map) -> CountryOutDTO:
    return CountryOutDTO(
        id=countrys_map[data.country_id].id,
        name=countrys_map[data.country_id].name,
        name_ua=countrys_map[data.country_id].name_ua,
        code=countrys_map[data.country_id].code,
        flag_emoji=countrys_map[data.country_id].flag_emoji,
        currency=countrys_map[data.country_id].currency,
    )


def _to_location_region(data, regions_map) -> RegionOutDTO:
    return RegionOutDTO(
        id=regions_map[data.region_id].id,
        name=regions_map[data.region_id].name,
        name_ua=regions_map[data.region_id].name_ua,
        country_id=regions_map[data.region_id].country_id,
    )


def _to_location_city(data, cities_map) -> CityOutDTO:
    return CityOutDTO(
        id=cities_map[data.city_id].id,
        name=cities_map[data.city_id].name,
        name_ua=cities_map[data.city_id].name_ua,
        country_id=cities_map[data.city_id].country_id,
        region_id=cities_map[data.city_id].region['id'],
        latitude=cities_map[data.city_id].latitude,
        longitude=cities_map[data.city_id].longitude,
    )


def _to_location_market(data, locations) -> LocationOutDTO:
    return LocationOutDTO(
        country=_to_location_country(data, locations["countries"]),
        region=_to_location_region(data, locations["regions"]),
        city=_to_location_city(data, locations["cities"]),
    )


def _to_market_out(data, locations) -> MarketFullOutDTO:
    return MarketFullOutDTO(
        id=data.id,
        name=data.name,
        address_line=data.address_line,
        location=_to_location_market(data.location, locations),
    )


# ==================================================================
