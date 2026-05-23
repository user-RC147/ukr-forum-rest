from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = "apps.shop"
    verbose_name = "Барахолка"

    def ready(self):
        import apps.shop.signals