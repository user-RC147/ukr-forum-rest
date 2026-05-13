from django.urls import path
from apps.geo.api import views

app_name = 'geo'

urlpatterns = [
    path('countries/', views.CountryListView.as_view(), name='countries'),
    path('regions/',   views.RegionListView.as_view(),  name='regions'),
    path('cities/',    views.CityListView.as_view(),    name='cities'),
]