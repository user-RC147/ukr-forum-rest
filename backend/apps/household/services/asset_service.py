from apps.household.selectors.asset_selector import AssetSelector
from apps.household.dto.asset_dto import AssetOutDTO, CreateAssetDTO,ListAssetDTO,Asset_Id_Group_OutDTO
from apps.household.dto.location_dto import CountryOutDTO, LocationOutDTO,RegionOutDTO,CityOutDTO
from apps.household.repositories.asset_repo import AssetRepo

from apps.users.contracts import get_user_contract
from apps.geo.contracts import get_country_contract,get_region_contract,get_city_contract


class AssetService:

    def __init__(self)->None:
        self._selector=AssetSelector()
        self._repository=AssetRepo()

        self._get_user_contract = get_user_contract()

        self._get_country = get_country_contract()
        self._get_region = get_region_contract()
        self._get_city = get_city_contract()


    def get_user_assets(self,user_id:int):
        return self._selector.get_available_assets(user_id)
    

    
    def get_list_asset(self,dto:ListAssetDTO,user_id:int)->Asset_Id_Group_OutDTO:
        asset_list=self._selector.get_list_asset(dto,user_id)

        countries=set()
        regions=set()
        cities=set()

        for item in asset_list:
            countries.add(item.location.country_id)
            regions.add(item.location.region_id)
            cities.add(item.location.city_id)

        countries = self._get_country.get_many(countries)
        regions=self._get_region.get_many(regions)
        cities = self._get_city.get_many(cities)

        locations= {'countries':countries,'regions':regions,'cities':cities}


        dto = [Asset_Id_Group_OutDTO(
            id=asset.id,
            name=asset.name,
            group_id=asset.group_id,
            location = _to_location_asset_out(asset,locations),
            address_line=asset.address_line,
            created_by_id=asset.created_by_id,
            created_at=asset.created_at
        )for asset in asset_list]
        
        return dto


    def create(self,dto:CreateAssetDTO,creator_user_id:int):
        #Перевірка користувача на права і на його існування
        #contract=creator_user_id

        asset=self._repository.createAsset(dto=dto,creator_user_id=creator_user_id)
        return asset


def _to_location_city_out(data,cities)->CityOutDTO:
    return CityOutDTO(
        id=cities[data.city_id].id,
        name=cities[data.city_id].name,
        name_ua=cities[data.city_id].name_ua,
        country_id=cities[data.city_id].country_id,
        region_id=cities[data.city_id].region['id'],
        latitude=cities[data.city_id].latitude,
        longitude=cities[data.city_id].longitude      
    )


def _to_location_region_out(data,regions)->RegionOutDTO:
    return RegionOutDTO(
        id=regions[data.region_id].id,
        name=regions[data.region_id].name,
        name_ua=regions[data.region_id].name_ua,
        country_id=regions[data.region_id].country_id
    )

def _to_location_country_out(data,countries)->CountryOutDTO:
    return CountryOutDTO(
        id=countries[data.country_id].id,
        name=countries[data.country_id].name,
        name_ua=countries[data.country_id].name_ua,
        code=countries[data.country_id].code,
        flag_emoji=countries[data.country_id].flag_emoji,
        currency=countries[data.country_id].currency
    )

def _to_location_asset_out(data,locations)->LocationOutDTO:
    return LocationOutDTO(
        country=_to_location_country_out(data.location,locations['countries']),
        region=_to_location_region_out(data.location,locations['regions']),
        city=_to_location_city_out(data.location,locations['cities'])
    )