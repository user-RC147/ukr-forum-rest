from django.db.models import F, Sum, Q

from apps.household.dto.market_dto import (
    Market_Id_OutDTO,
    MarketExpenseOutDTO,
    MarketFullOutDTO,
    MarketExpense_Id_OutDTO,
)

from apps.household.dto.location_dto import LocationOutDTO,Location_Id_InDTO,Location_Id_OutDTO,LocationShortOutDTO

from apps.household.models import purchase, purchase_item
from apps.household.models.market import Market

from apps.household.models.purchase_item import PurchaseItem

from core.paginator.dto import PaginatorDTO
from core.paginator.paginator import paginate



class MarketSelector:

    def get_market_expenses(
        self,
        user_id: int,
        page: int,
        page_size: int,
        date_from: str | None,
        date_to: str | None,
    ) -> PaginatorDTO[MarketExpense_Id_OutDTO]:

        groups_market = PurchaseItem.objects.filter(
            Q(purchase__asset__group__members__user_id=user_id)
            | Q(purchase__asset__group__created_by_id=user_id)
        ).distinct()

        if date_from and date_to:
            groups_market = groups_market.filter(
                purchase__data_purchase__gte=date_from,
                purchase__data_purchase__lte=date_to,
            )
        

        groups_market = groups_market.values(
            market_id=F("purchase__market"),
            market_name=F("purchase__market__name"),
            market_address_line=F("purchase__market__address_line"),
            country_id=F("purchase__market__country_id"),
            region_id=F("purchase__market__region_id"),
            city_id=F("purchase__market__city_id"),
        ).annotate(total=Sum(F("price_per_unit") * F("quantity")))

        count = groups_market.count()

        

        offset = (page - 1) * page_size

        page_items = groups_market[offset : offset + page_size]

        dto = [_to_dto_out_groups_market(item) for item in page_items]

        paginator_pages = paginate(dto, count, page, page_size)

     

        return paginator_pages

    def get_all(self):
        markets = Market.objects.all()

        dto_markets = [
            Market_Id_OutDTO(
                id=market.id,
                name=market.name,
                address_line=market.address_line,
                location=Location_Id_InDTO(
                    country_id=market.country_id,
                    region_id=market.region_id,
                    city_id=market.city_id,
                ),
            )
            for market in markets
        ]

        return dto_markets


# [{'purchase__market': 2, 'purchase__market__name': 'Edeka', 'total': Decimal('264.00000')}]>

def _to_dto_location_id(data) -> Location_Id_OutDTO:
    return Location_Id_OutDTO(
        country_id=data['country_id'],
        region_id=data['region_id'],
        city_id=data['city_id']
    )


def _to_dto_out_groups_market(data) -> MarketExpense_Id_OutDTO:
    return MarketExpense_Id_OutDTO(
        id=data['market_id'],
        name=data['market_name'],
        location=_to_dto_location_id(data),
        address_line=data['market_address_line'],
        total=data['total'],
        
    )
