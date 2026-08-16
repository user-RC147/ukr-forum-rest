# apps/geo/admin.py
from django.contrib import admin

from apps.geo.models.city_model import CityModel
from apps.geo.models.country_model import CountryModel
from apps.geo.models.region_model import RegionModel


@admin.register(CountryModel)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "flag_emoji", "name", "name_ua", "code", "currency"]
    search_fields = ["name", "name_ua", "code"]
    ordering = ["name"]


@admin.register(RegionModel)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "name_ua", "country", "api_id"]
    search_fields = ["name", "name_ua"]
    list_filter = ["country"]
    ordering = ["country__name", "name"]


@admin.register(CityModel)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "name_ua", "country", "region", "api_id"]
    search_fields = ["name", "name_ua"]
    list_filter = ["country", "region"]
    ordering = ["country__name", "region__name", "name"]
