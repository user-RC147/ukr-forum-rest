from django.apps import AppConfig


class HouseholdConfig(AppConfig):
    name = "apps.household"
    verbose_name = "Сімейні витрати"

    # Внутрішні кеш-змінні для Singleton-об'єктів
    _market_service = None
    _asset_service = None
    _product_service = None
    _purchase_service = None
    _group_service = None

    @property
    def asset_service(self):
        if self._asset_service is None:
            from apps.household.selectors import AssetSelector
            from apps.household.services import AssetService
            from apps.household.repositories import AssetRepo

            asset_selector = AssetSelector()
            self._asset_service = AssetService(
                selector=asset_selector,
                repository=AssetRepo()
                )
        return self._asset_service

    @property
    def market_service(self):
        if self._market_service is None:
            from apps.geo.apps import GeoConfig
            from apps.household.repositories import MarketRepo
            from apps.household.selectors import MarketSelector
            from apps.household.services import MarketService

            # Навіть якщо geo запустився пізніше, у цей момент
            # (коли пішов перший запит до API) його сервіс вже точно готовий!
            geo_service_contract = GeoConfig.service

            self._market_service = MarketService(
                repository=MarketRepo(),
                selector=MarketSelector(),
                geo_service=geo_service_contract,
            )
        return self._market_service

    @property
    def product_service(self):
        if self._product_service is None:
            from apps.household.repositories import ProductRepo
            from apps.household.selectors import ProductSelector
            from apps.household.services import ProductService

            self._product_service = ProductService(
                repository=ProductRepo(), selector=ProductSelector()
            )
        return self._product_service

    @property
    def purchase_service(self):
        if self._purchase_service is None:
            from apps.household.repositories import PurchaseRepo
            from apps.household.selectors import GroupSelector
            from apps.household.services import PurchaseService

            self._purchase_service = PurchaseService(
                repository=PurchaseRepo(), group_selector=GroupSelector()
            )
        return self._purchase_service

    @property
    def group_service(self):
        if self._group_service is None:
            from apps.household.repositories import GroupRepo
            from apps.household.selectors import GroupSelector
            from apps.household.services import GroupService

            self._group_service = GroupService(
                group_repo=GroupRepo(), group_selector=GroupSelector()
            )
        return self._group_service
