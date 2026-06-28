from rest_framework import routers

from .views import CategoryView, SearchView, TagView

APP_NAME = "search"

router = routers.SimpleRouter()
router.register(r"", SearchView, basename="search")
router.register(r"category", CategoryView, basename="category")
router.register(r"tag", TagView, basename="tag")
urlpatterns = router.urls
