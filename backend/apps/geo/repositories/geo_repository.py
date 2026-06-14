# apps/geo/repositories/geo_repository.py
from apps.geo.models import Country, Region, City
from typing import Optional
from django.db.models.manager import BaseManager

class GeoRepository:

    def get_or_create_country(self, api_data: dict) -> Country:
        country, _ = Country.objects.get_or_create(
            code=api_data['code'],
            defaults={
                'name':       api_data['name'],
                'name_ua':    api_data.get('name_translate', ''),
                'flag_emoji': api_data.get('flag_emoji', ''),
                'currency':   api_data.get('currency'),
            }
        )
        return country

    def get_or_create_region(self, api_data: dict, country: Country) -> Region:
        region, _ = Region.objects.get_or_create(
            api_id=api_data['id'],  # ← зовнішній id зберігаємо в api_id
            defaults={
                'name':    api_data['name'],
                'name_ua': api_data.get('name_translate', ''),
                'country': country,
            }
        )
        return region

    def get_or_create_city(self, api_data: dict, country: Country, region: Region) -> City:
        city, _ = City.objects.get_or_create(
            api_id=api_data['id'],  # ← зовнішній id зберігаємо в api_id
            defaults={
                'name':      api_data['name'],
                'name_ua':   api_data.get('name_translate', ''),
                'country':   country,
                'region':    region,
                'latitude':  api_data.get('latitude'),
                'longitude': api_data.get('longitude'),
            }
        )
        return city


#=====
# Додати всередину класу GeoRepository у файлі apps/geo/repositories/geo_repository.py:

    def get_country_by_code(self, code: str) -> Optional[Country]:
        return Country.objects.filter(code=code).first()

    def get_region_by_id_with_country(self, region_id: int) -> Optional[Region]:
        return Region.objects.select_related('country').filter(id=region_id).first()

    def get_city_by_id(self, city_id: int) -> Optional[City]:
        return City.objects.filter(id=city_id).first()

    def country_exists(self, country_id: int) -> bool:
        return Country.objects.filter(id=country_id).exists()

    def region_exists(self, region_id: int) -> bool:
        return Region.objects.filter(id=region_id).exists()

    def city_exists(self, city_id: int) -> bool:
        return City.objects.filter(id=city_id).exists()
    
    def get_countries(self, ids: list[int]) -> BaseManager[Country]:
        return Country.objects.filter(id__in=ids)
    
    def get_regions(self, ids: list[int]) -> BaseManager[Region]:
        return Region.objects.filter(id__in=ids)
    
    def get_cities(self, ids: list[int]) -> BaseManager[City]:
        return City.objects.filter(id__in=ids)
#=====



geo_repository = GeoRepository()