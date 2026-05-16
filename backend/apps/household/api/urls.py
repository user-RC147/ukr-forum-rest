# apps/household/api/urls.py
from rest_framework.routers import DefaultRouter
from apps.household.api.views.asset import AssetViewSet
#from apps.household.api.views.group import GroupViewSet
from apps.household.api.views.market import MarketViewSet
#from apps.household.api.views.product import ProductViewSet
from apps.household.api.views.purchase import PurchaseViewSet

router = DefaultRouter()
#router.register('groups',    GroupViewSet,    basename='group')
router.register('assets',    AssetViewSet,    basename='asset')
router.register('markets',   MarketViewSet,   basename='market')
#router.register('products',  ProductViewSet,  basename='product')
router.register('purchases', PurchaseViewSet, basename='purchase')

urlpatterns = router.urls