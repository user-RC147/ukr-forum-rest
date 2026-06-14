from rest_framework import routers

from .views import SearchView

APP_NAME = "search"

router = routers.SimpleRouter()
router.register(r"", SearchView, basename="search")
urlpatterns = router.urls
