from rest_framework.routers import DefaultRouter

from apps.users.api.views import (
    RefreshViewSet,
    CsrfViewSet,
    LoginViewSet,
    PasswordResetViewSet,LogoutViewSet
)
from apps.users.api.views.confirm_email_view import ConfirmEmailView

router = DefaultRouter()



router.register("confirm-email", ConfirmEmailView, basename="confirm-email")
router.register("login", LoginViewSet, basename="login")
router.register("logout", LogoutViewSet, basename="logout")
router.register("refresh", RefreshViewSet, basename="refresh")
router.register("csrf", CsrfViewSet, basename="csrf")

router.register("password-reset", PasswordResetViewSet, basename="password-reset")


urlpatterns = router.urls
