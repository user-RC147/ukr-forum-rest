from rest_framework.routers import DefaultRouter

from apps.users.api.views import RefreshViewSet,CsrfViewSet,LoginViewSet


router=DefaultRouter()


router.register("login", LoginViewSet, basename="login")
router.register("refresh", RefreshViewSet, basename="refresh")
router.register("csrf", CsrfViewSet, basename="csrf")


urlpatterns =router.urls
