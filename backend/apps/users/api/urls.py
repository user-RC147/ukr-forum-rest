from rest_framework.routers import DefaultRouter

from apps.users.api.views.user_view import UserViewSet
from apps.users.api.views.star_view import StarPageViewSet

router = DefaultRouter()

router.register('star',StarPageViewSet,basename='star')
router.register("", UserViewSet, basename="users")



urlpatterns = router.urls
