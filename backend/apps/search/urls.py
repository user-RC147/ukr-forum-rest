from rest_framework import routers

from .views import CategoryView, SearchView

APP_NAME = "search"

router = routers.SimpleRouter()
router.register(r"", SearchView, basename="search")
router.register(r"category", CategoryView, basename="category")
urlpatterns = router.urls
