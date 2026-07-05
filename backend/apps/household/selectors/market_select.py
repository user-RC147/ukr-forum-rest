from apps.household.dto.market_dto import MarketOutDTO
from apps.household.models.market import Market



class MarketSelector:
    
    def get_all(self):
        markets=Market.objects.all()
        

        dto_markets = [MarketOutDTO(
            id=market.id,
            name=market.name,
            address_line=market.address_line,
            country_id=market.country_id,
            region_id=market.region_id,
            city_id=market.city_id,
        ) for market in markets]


        
        return dto_markets