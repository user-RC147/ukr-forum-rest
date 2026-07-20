from apps.household.dto.asset_dto import AssetOutDTO
from apps.household.dto.group_dto import GroupOutDTO, GroupMemberOutDTO
from apps.household.dto.location_dto import (
    CityOutDTO,
    CountryOutDTO,
    LocationOutDTO,
    RegionOutDTO,
)
from apps.household.dto.market_dto import MarketFullOutDTO
from apps.household.dto.purchase_dto import (
    CreatePurchaseInDTO,
    PurchaseItemOutDTO,
    PurchaseOutDTO,
    Purchase_Id_Name_OutDTO,
)

# ПОЯСНЕННЯ ДІЇ: Використовуємо створені нами точки входу (__init__.py -> __all__)
# Тепер нам не треба писати довжелезні шляхи до кожного окремого файлу.
from apps.household.repositories.purchase_repo import PurchaseRepo
from apps.household.selectors.group_selector import GroupSelector

from apps.geo.contracts import (
    get_city_contract,
    get_region_contract,
    get_country_contract,
)
from apps.household.selectors.purchase_selector import PurchaseSelector
from apps.household.dto.user_dto import UserOutDTO
from apps.household.dto.role_dto import RoleOutDTO

from dataclasses import fields
from apps.users.contracts.user_contract import get_user_contract

from apps.users.dto.user import UserDTO


class PurchaseService:
    """
    Сервіс для управління бізнес-логікою чеків.
    Об'єднує перевірку прав доступу групи та запис чека в базу даних.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._repository = PurchaseRepo()
        self._group_selector = GroupSelector()
        self._selector = PurchaseSelector()

        self._get_user_contract = get_user_contract()

        self._get_country_contract = get_country_contract()
        self._get_region_contract = get_region_contract()
        self._get_city_contract = get_city_contract()

    def get_location_full(self, item):
        location = LocationOutDTO(
            country=CountryOutDTO(
                id=item.country.id,
                name=item.country.name,
                name_ua=item.country.name_ua,
                code=item.country.code,
                flag_emoji=item.country.flag_emoji,
                currency=item.country.currency,
            ),
            region=RegionOutDTO(
                id=item.region.id,
                name=item.region.name,
                name_ua=item.region.name_ua,
                country_id=item.region.country_id,
            ),
            city=CityOutDTO(
                id=item.city.id,
                name=item.city.name,
                name_ua=item.city.name_ua,
                country_id=item.city.country_id,
                region_id=item.city.region_id,
                latitude=item.city.latitude,
                longitude=item.city.longitude,
            ),
        )

        return location

    def _get_locations_geo(self, data) -> dict[LocationOutDTO]:
        countries = set()
        regions = set()
        cities = set()

        for item in data:
            countries.add(item.asset.location.country_id)
            countries.add(item.market.location.country_id)
            regions.add(item.asset.location.region_id)
            regions.add(item.market.location.region_id)
            cities.add(item.asset.location.city_id)
            cities.add(item.market.location.city_id)

        countries = self._get_country_contract.get_many(list(countries))
        regions = self._get_region_contract.get_many(list(regions))
        cities = self._get_city_contract.get_many(list(cities))

        locations = {"countries": countries, "regions": regions, "cities": cities}

        return locations

    def get_all_purchase(self, user_id: int) -> list[PurchaseOutDTO]:

        purchase_list = self._selector.get_all_purchase(user_id=user_id)

        user_map = _get_user_contract(purchase_list)

        locations_asset_and_makret = self._get_locations_geo(purchase_list)
        
        dto = [
            PurchaseOutDTO(
                id=purchase.id,
                data_purchase=purchase.data_purchase,
                note=purchase.note,
                asset=_dto_asset_out(
                    purchase.asset, locations=locations_asset_and_makret,user_map=user_map
                ),
                market=_dto_market_dto(
                    purchase.market, locations=locations_asset_and_makret
                ),
                created_at=purchase.created_at,
                created_by_id=purchase.created_by_id,
                items=purchase.items,
                # Фінансовий підсумок чека
                total_amount=purchase.total_amount,
            )
            for purchase in purchase_list
        ]

        return dto

    def create(self, dto: CreatePurchaseInDTO, creator_user_id: int) -> PurchaseOutDTO:
        """
        Бізнес-процес створення чека з попередньою перевіркою ролей учасника.
        """
        create_purchase = self._repository.create(
            dto=dto, creator_user_id=creator_user_id
        )

        countries = {
            create_purchase.asset.location.country.id,
            create_purchase.market.location.country.id,
        }
        regions = {
            create_purchase.asset.location.region.id,
            create_purchase.market.location.region.id,
        }

        cities = {
            create_purchase.asset.location.city.id,
            create_purchase.market.location.city.id,
        }

        countries = self._get_country_contract.get_many(list(countries))
        regions = self._get_region_contract.get_many(list(regions))
        cities = self._get_city_contract.get_many(list(cities))

        new_create_purchase = PurchaseOutDTO(
            id=create_purchase.id,
            data_purchase=create_purchase.data_purchase,
            note=create_purchase.note,
            asset=AssetOutDTO(
                id=create_purchase.asset.id,
                name=create_purchase.asset.name,
                group=create_purchase.asset.group,
                location=self.get_location_full(create_purchase.asset),
                address_line=create_purchase.asset.address_line,
                created_by_id=create_purchase.created_by_id,
                created_at=create_purchase.created_at,
            ),
            market=MarketFullOutDTO(
                id=create_purchase.market.id,
                name=create_purchase.market.name,
                address_line=create_purchase.market.address_line,
                location=self.get_location_full(create_purchase.market),
            ),
            created_at=create_purchase.created_at,
            created_by_id=create_purchase.created_by_id,
            items=create_purchase.items,
            # Фінансовий підсумок чека
            total_amount=create_purchase.total_amount,
        )

        return new_create_purchase


def _get_user_contract(data):
    users_ids = set()

    for item in data:
        for member in item.asset.group.members:
            users_ids.add(member.user_id)

    user_map =get_user_contract().get_many(users_ids)
    
    return user_map


def _dto_user_out(data,user_map) -> UserOutDTO:
    return UserOutDTO(
        id=user_map[data.created_by_id].id,
        username=user_map[data.created_by_id].username,
        display_name=user_map[data.created_by_id].display_name
    )


def _dto_role_out(data) -> RoleOutDTO:
    return RoleOutDTO(
        id=data.id, name=data.name, name_ua=data.name_ua, is_bool=data.is_bool
    )


def _dto_group_members(data) -> GroupMemberOutDTO:
    return GroupMemberOutDTO(
        id=data.id,
        group_id=data.group_id,
        user_id=data.user_id,
        role=_dto_role_out(data.rele),
        joined_at=data.joined_at,
    )


def _dto_group_out(data,user_map) -> GroupOutDTO:
    return GroupOutDTO(
        id=data.id,
        name=data.name,
        created_by=_dto_user_out(data,user_map),
        created_at=data.created_at,
        members=data.members,
    )


def _dto_location_country(data, countrys_map) -> CountryOutDTO:
    return CountryOutDTO(
        id=countrys_map[data.country_id].id,
        name=countrys_map[data.country_id].name,
        name_ua=countrys_map[data.country_id].name_ua,
        code=countrys_map[data.country_id].code,
        flag_emoji=countrys_map[data.country_id].flag_emoji,
        currency=countrys_map[data.country_id].currency,
    )


def _dto_location_region(data, regions_map) -> RegionOutDTO:
    return RegionOutDTO(
        id=regions_map[data.region_id].id,
        name=regions_map[data.region_id].name,
        name_ua=regions_map[data.region_id].name_ua,
        country_id=regions_map[data.region_id].country_id,
    )


def _dto_location_city(data, cities_map) -> CityOutDTO:
    return CityOutDTO(
        id=cities_map[data.city_id].id,
        name=cities_map[data.city_id].name,
        name_ua=cities_map[data.city_id].name_ua,
        country_id=cities_map[data.city_id].country_id,
        region_id=cities_map[data.city_id].region["id"],
        latitude=cities_map[data.city_id].latitude,
        longitude=cities_map[data.city_id].longitude,
    )


def _dto_location_out(data, locations) -> LocationOutDTO:
    return LocationOutDTO(
        country=_dto_location_country(data, locations["countries"]),
        region=_dto_location_region(data, locations["regions"]),
        city=_dto_location_city(data, locations["cities"]),
    )


def _dto_asset_out(data, locations,user_map) -> AssetOutDTO:
    return AssetOutDTO(
        id=data.id,
        name=data.name,
        group=_dto_group_out(data.group,user_map),
        location=_dto_location_out(data.location, locations),
        address_line=data.address_line,
        created_by_id=data.created_by_id,
        created_at=data.created_at,
    )


def _dto_market_dto(data, locations) -> MarketFullOutDTO:
    return MarketFullOutDTO(
        id=data.id,
        name=data.name,
        address_line=data.address_line,
        location=_dto_location_out(data.location, locations),
    )


def _dto_items(data: Purchase_Id_Name_OutDTO) -> PurchaseItemOutDTO:
    return PurchaseItemOutDTO(items=data)


# PurchaseItemOutDTO(
#         id:int
#         purchase_id:int
#         product:ProductOutDTO
#         quantity:Decimal
#         price_per_unit:Decimal
#         total_price:Decimal
#     )
