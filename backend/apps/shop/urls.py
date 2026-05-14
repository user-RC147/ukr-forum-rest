from django.urls import path
from rest_framework import routers
from .views import ProductViewSet

APP_NAME = "shop"

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet, basename='products')
urlpatterns = router.urls