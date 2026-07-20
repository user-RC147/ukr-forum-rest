from apps.household.dto.market_dto import Market_Id_OutDTO, MarketFullOutDTO
from apps.household.models.market import Market
from apps.household.dto.location_dto import LocationIdInDTO


class MarketSelector:

    def get_all(self):
        markets = Market.objects.all()

        dto_markets = [
            Market_Id_OutDTO(
                id=market.id,
                name=market.name,
                address_line=market.address_line,
                location=LocationIdInDTO(
                    country_id=market.country_id,
                    region_id=market.region_id,
                    city_id=market.city_id,
                ),
            )
            for market in markets
        ]

        return dto_markets
