# apps/geo/admin.py
from django.contrib import admin

from apps.geo.cache_keys import (
    city_by_region_cache_key,
    country_cache_key,
    region_by_country_cache_key,
)
from apps.geo.models.city_model import CityModel
from apps.geo.models.country_model import CountryModel
from apps.geo.models.region_model import RegionModel
from core.cache.cache_invalidation import (
    CacheInvalidationAdminMixin,
    DynamicCacheInvalidationAdminMixin,
)


@admin.register(CountryModel)
class CountryAdmin(CacheInvalidationAdminMixin, admin.ModelAdmin):
    cache_key = country_cache_key()
    list_display = ["id", "flag_emoji", "name", "name_ua", "code", "currency"]
    search_fields = ["name", "name_ua", "code"]
    ordering = ["name"]


@admin.register(RegionModel)
class RegionAdmin(DynamicCacheInvalidationAdminMixin, admin.ModelAdmin):
    cache_key_field = "country_id"
    cache_key_builder = staticmethod(region_by_country_cache_key)
    list_display = ["id", "name", "name_ua", "country", "api_id"]
    search_fields = ["name", "name_ua"]
    list_filter = ["country"]
    ordering = ["country__name", "name"]


@admin.register(CityModel)
class CityAdmin(DynamicCacheInvalidationAdminMixin, admin.ModelAdmin):
    cache_key_field = "region_id"
    cache_key_builder = staticmethod(city_by_region_cache_key)
    list_display = ["id", "name", "name_ua", "country", "region", "api_id"]
    search_fields = ["name", "name_ua"]
    list_filter = ["country", "region"]
    ordering = ["country__name", "region__name", "name"]
