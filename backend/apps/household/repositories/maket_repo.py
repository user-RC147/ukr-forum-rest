from typing import Optional
from apps.household.models.market import Market
from apps.household.dto.market_dto import CreateMarketInDTO

class MarketRepo:


    def create(self,dto:CreateMarketInDTO,user_id:int)->Market:
        """
        Репозиторій відповідає ТІЛЬКИ за запис і зміну даних (Команди).
        """

        market = Market.objects.create(
            name=dto.name,
            address_line=dto.address_line,
            country_id=dto.country_id,
            region_id=dto.region_id,
            city_id=dto.city_id,
            created_by_id=user_id,
        )

        return market
    
    def update(self, market_id:int, dto:CreateMarketInDTO)->Optional[Market]:
        # Логіка оновлення об'єкта
        pass


    def delete(self,market_id:int)->bool:
        # Логіка видалення
        deleted_count, _ =Market.objects.filter(id=market_id).delete()
        return deleted_count > 0