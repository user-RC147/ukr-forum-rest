from rest_framework.routers import DefaultRouter

from apps.users.api.views.login_view import LoginViewSet
from apps.users.api.views.refresh_view import RefreshViewSet


router=DefaultRouter()


router.register('login',LoginViewSet,basename='login')
router.register('refresh',RefreshViewSet,basename='refresh')


urlpatterns =router.urls
