# apps/geo/repositories/geo_repository.py
from apps.geo.models import Country, Region, City
from typing import Optional
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest

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
    
    def search_country(self, query: str, limit: int) -> QuerySet[Country]:
        return (
            Country.objects.all()
            .only("id", "name", "name_ua")
            .annotate(
                similarity=Greatest(
                    TrigramSimilarity("name", query),
                    TrigramSimilarity("name_ua", query),
                )
            )
            .filter(
                Q(name__istartswith=query)
                | Q(name_ua__istartswith=query)
                | Q(similarity__gt=0.3)
            )
            .order_by("-similarity", "name")[:limit]
        )
    
    def search_city(self, query: str, country_id: int, limit: int) -> QuerySet[City]:
        return (
            City.objects.all()
            .only("id", "name", "name_ua")
            .annotate(
                similarity=Greatest(
                    TrigramSimilarity("name", query),
                    TrigramSimilarity("name_ua", query),
                )
            )
            .filter(
                Q(name__istartswith=query)
                | Q(name_ua__istartswith=query)
                | Q(similarity__gt=0.3)
                | Q(country__id=country_id)
            )
            .order_by("-similarity", "name")[:limit]
        )
#=====



geo_repository = GeoRepository()