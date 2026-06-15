from typing import Any

from pytest import mark
from core.contracts.geo import IGeoServiceContract


from apps.household.dto.market_dto import CreateMarketInDTO
from apps.household.repositories.maket_repo import MarketRepo
from apps.household.selectors.market_select import MarketSelector



class MarketService:
    """
    Бізнес-логіка для роботи з магазинами (Markets).
    Реалізує гнучку перевірку гео-локації через зовнішній контракт модулів.
    """

    def __init__(self, 
                 repository:MarketRepo,
                 geo_service:IGeoServiceContract,
                 selector:MarketSelector,
                 )->None:
        # Залежності заходять сюди з HouseholdConfig.ready()
        self._repository=repository
        self._selector=selector
        self._geo_service=geo_service



    def get_all_markets(self,
                        search_query=None,
                        country_id=None,
                        region_id=None,
                        city_id=None,
                        ordering=None
                        ):
        
        # 1. Забираємо базовий список магазинів через селектор
        market_all_list = self._selector.get_market_list(
            search_query=search_query,
            country_id=country_id,
            region_id=region_id,
            city_id=city_id,
            ordering=ordering
        )

        if not market_all_list:
            return []

        # 2. Збираємо унікальні ID (виправлено помилку з countery_id)
        country_ids = list({m.country_id for m in market_all_list if m.country_id})
        region_ids = list({m.region_id for m in market_all_list if m.region_id})
        box_city_ids = list({m.city_id for m in market_all_list if m.city_id})

        # 3. Викликаємо РЕАЛЬНІ методи вашого GeoService замість неіснуючого get_name_by_ids
        countries_dtos = self._geo_service.get_countries(country_ids)
        regions_dtos = self._geo_service.get_regions(region_ids)
        cities_dtos = self._geo_service.get_cities(box_city_ids)

        # 4. Перетворюємо списки DTO на зручні словники (мапи) типу {id: name}
        # Використовуємо .name_ua (або .name, якщо потрібна оригінальна назва)
        countries_map = {c.id: c.name_ua for c in countries_dtos}
        regions_map = {r.id: r.name_ua for r in regions_dtos}
        cities_map = {c.id: c.name_ua for c in cities_dtos}

        # 5. Динамічно збагачуємо об'єкти моделей Market перед передачею в серіалізатор
        for market in market_all_list:
            market.country_name = countries_map.get(market.country_id, None)
            market.region_name = regions_map.get(market.region_id, None)
            market.city_name = cities_map.get(market.city_id, None)

        return market_all_list

    # def get_all_markets(self,
    #                     search_query=None,
    #                     country_id=None,
    #                     region_id=None,
    #                     city_id=None,
    #                     ordering=None
    #                     ):
        
    #     # 1. Забираємо базовий список магазинів через репозиторій/селектор
    #     # Примітка: у вашому коді в сервісі викликається self._repository.get_market_list, 
    #     # хоча логіка написана в MarketSelector. Переконайтеся, що викликаєте саме селектор: self.selector.get_market_list(...)
    #     market_all_list=self._selector.get_market_list(
    #         search_query=search_query,
    #         country_id=country_id,
    #         region_id=region_id,
    #         city_id=city_id,
    #         ordering=ordering
    #     )

    #     if not market_all_list:
    #         return []
    #     # 2. Збираємо унікальні ID для передачі в контракт (фільтруємо None значення)
    #     country_ids=list({m.countery_id for m in market_all_list if m.country_id})
    #     region_ids=list({m.region_id for m in market_all_list if m.region_id})
    #     box_city_ids =list({m.city_id for m in market_all_list if m.city_id})

    #     # 3. Йдемо через контракт в інший модуль Geo (ОДИН запит на весь список)
    #     # Очікуємо, що гео-сервіс поверне структуру з мапами: {country_id: "Назва", ...}
    #     geo_data=self._geo_service.get_name_by_ids(
    #         country_ids=country_ids,
    #         region_ids=region_ids,
    #         city_ids=box_city_ids
    #     )

    #     # Дістаємо мапи або створюємо пусті дефолти, якщо контракт повернув None
    #     countries_map=geo_data.get('countries',{})
    #     regions_map=geo_data.get('regions',{})
    #     cities_map=geo_data.get('cities',{})

    #     # 4. Динамічно збагачуємо (мутуємо) об'єкти перед передачею в серіалізатор
    #     for market in market_all_list:
    #         # Навішуємо нові атрибути прямо на Django-модель у пам'яті Python
    #         market.country_name=countries_map.get(market.country_id,None)
    #         market.region_name=regions_map.get(market.region_id,None)
    #         market.city_name=cities_map.get(market.city_id,None)


    #     return market_all_list
    
    def create(self,dto:CreateMarketInDTO,user)->Any:
        """
        Створює магазин із покроковою гнучкою валідацією локації.
        Користувач може обрати лише країну, країну+регіон або повний ланцюжок.
        """
        # 1. Якщо передано country_id — валідуємо через гео-сервіс
        if dto.country_id is not None:
            if not self._geo_service.is_country_exists(dto.country_id):
                raise ValueError("Вказана країна не існує в системі.")
            
            # 2. Якщо передано region_id — валідуємо регіон
            if dto.region_id is not None:
                if not self._geo_service.is_region_exists(dto.region_id):
                    raise ValueError("Вказаний регіон не існує в системі.")
                
            # 3. Якщо передано city_id — валідуємо місто
            if dto.city_id is not None:
                if not self._geo_service.is_city_exists(dto.city_id):
                    raise ValueError("Вказане місто не існує в системі.")
            
            # 4. Якщо всі перевірки пройшли успішно, передаємо DTO далі в репозиторій для збереження
            return self._repository.create(dto=dto, user_id=user.id)
