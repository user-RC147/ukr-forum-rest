from typing import Any
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
        self.selector=selector
        self._geo_service=geo_service


    def get_all_markets(self,
                        search_query=None,
                        country_id=None,
                        region_id=None,
                        city_id=None,
                        ordering=None
                        ):
        
        # Делегуємо задачу селектору
        market_all_list=self._repository.get_market_list(
            search_query=search_query,
            country_id=country_id,
            region_id=region_id,
            city_id=city_id,
            ordering=ordering
        )

        return market_all_list
    
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
