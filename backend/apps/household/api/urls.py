# apps/household/api/urls.py
from rest_framework.routers import DefaultRouter
from apps.household.api.views.asset_view import AssetViewSet
from apps.household.api.views.group_user_view import GroupViewSet
from apps.household.api.views.market_view import MarketViewSet
from apps.household.api.views.product_view import ProductViewSet
from apps.household.api.views.purchase_view import PurchaseViewSet
from apps.household.api.views.unit_of_measure_view import UnitOfMeasureViewSet

router = DefaultRouter()
router.register('groups',    GroupViewSet,    basename='group')
router.register('assets',    AssetViewSet,    basename='asset')
router.register('markets',   MarketViewSet,   basename='market')
router.register('unit-of-measure', UnitOfMeasureViewSet, basename='unit-of-measure')
router.register('products',  ProductViewSet,  basename='product')
router.register('purchases', PurchaseViewSet, basename='purchase')

urlpatterns = router.urls