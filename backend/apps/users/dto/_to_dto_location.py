from core.dto.geo.location_dto import (
    Location_Id_OutDTO,
    LocationOutDTO,
)
from apps.geo.dto.country import CountryDTO
from apps.geo.dto.region import RegionDTO
from apps.geo.dto.city import CityDTO,City_id_region_DTO

def _to_dto_out_contry(data, map_location) -> CountryDTO:
    return CountryDTO(
        id=map_location['countries'][data.country_id].id,
        name=map_location['countries'][data.country_id].name,
        name_ua=map_location['countries'][data.country_id].name_ua,
        code=map_location['countries'][data.country_id].code,
        flag_emoji=map_location['countries'][data.country_id].flag_emoji,
        currency=map_location['countries'][data.country_id].currency,
    )


def _to_dto_out_region(data, map_location) -> RegionDTO:
    return RegionDTO(
        id=map_location['regions'][data.region_id].id,
        name=map_location['regions'][data.region_id].name,
        name_ua=map_location['regions'][data.region_id].name_ua,
        country_id=map_location['regions'][data.region_id].country_id,
    )


def _to_dto_out_city(data, map_location) -> City_id_region_DTO:
    return City_id_region_DTO(
        id=map_location['cities'][data.city_id].id,
        name=map_location['cities'][data.city_id].name,
        name_ua=map_location['cities'][data.city_id].name_ua,
        country_id=map_location['cities'][data.city_id].country_id,
        region_id=map_location['cities'][data.city_id].region.id,
        latitude=map_location['cities'][data.city_id].latitude,
        longitude=map_location['cities'][data.city_id].longitude,
    )


# country_id: int,
#     region_id: int,
#     city_id: int,

def _to_dto_out_id_location(data) -> Location_Id_OutDTO:
    return Location_Id_OutDTO(
        country_id=data.country_id,
        region_id=data.region_id,
        city_id=data.city_id,
    )


def _to_dto_out_location(data, map_location) -> LocationOutDTO:
    return LocationOutDTO(
        country=_to_dto_out_contry(data, map_location),
        region=_to_dto_out_region(data, map_location),
        city=_to_dto_out_city(data, map_location),
    )


def _get_ids_location(data) -> dict:

    if not isinstance(data, list):
        data = [data]

    country_ids = set()
    region_ids = set()
    city_ids = set()

    for item in data:
        if item.location is None:
            continue
        country_ids.add(item.location.country_id)
        region_ids.add(item.location.region_id)
        city_ids.add(item.location.city_id)

    return {"country_ids": country_ids, "region_ids": region_ids, "city_ids": city_ids}


def _get_locations(ids: list[dict], countries, regions, cities):

    countries = countries.get_many(ids["country_ids"])
    regions = regions.get_many(ids["region_ids"])
    cities = cities.get_many(ids["city_ids"])

    locations = {"countries": countries, "regions": regions, "cities": cities}

    return locations
