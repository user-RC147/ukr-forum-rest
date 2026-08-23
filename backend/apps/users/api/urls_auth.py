from rest_framework.routers import DefaultRouter

from apps.users.api.views import (
    RefreshViewSet,
    CsrfViewSet,
    LoginViewSet,
    PasswordResetViewSet,
)

router = DefaultRouter()


router.register("login", LoginViewSet, basename="login")
router.register("refresh", RefreshViewSet, basename="refresh")
router.register("csrf", CsrfViewSet, basename="csrf")

router.register("password-reset", PasswordResetViewSet, basename="password-reset")


urlpatterns = router.urls
