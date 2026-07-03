from django.urls import path
from apps.geo.api.views.resolve import GeoResolveView
from apps.geo.api.views.countries import CountryListView, CountrySearchView
from apps.geo.api.views.regions import RegionListView
from apps.geo.api.views.cities import CityListView, CitySearchView

urlpatterns = [
    path('resolve/',   GeoResolveView.as_view(),  name='geo-resolve'),
    path('countries/', CountryListView.as_view(), name='geo-countries'),
    path('countries/search/', CountrySearchView.as_view(), name='geo-countries-search'),
    path('regions/',   RegionListView.as_view(),  name='geo-regions'),
    path('cities/',    CityListView.as_view(),    name='geo-cities'),
    path('cities/search/',    CitySearchView.as_view(),    name='geo-cities-search'),
]