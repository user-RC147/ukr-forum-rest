from rest_framework import routers

from .views.city_views import CityView
from .views.country_views import CountryView
from .views.region_views import RegionView

APP_NAME = "geo"

router = routers.SimpleRouter()
router.register(r"country", CountryView, basename="country")
router.register(r"city", CityView, basename="city")
router.register(r"region", RegionView, basename="region")
urlpatterns = router.urls
