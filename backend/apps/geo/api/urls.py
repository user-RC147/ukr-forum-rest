from rest_framework import routers

from apps.geo.api.geo_views import CityView, CountryView, RegionView

APP_NAME = "geo"

router = routers.SimpleRouter()
router.register(r"country", CountryView, basename="country")
router.register(r"city", CityView, basename="city")
router.register(r"region", RegionView, basename="region")
urlpatterns = router.urls
