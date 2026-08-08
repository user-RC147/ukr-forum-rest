from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = "apps.shop"
    verbose_name = "Барахолка"

    def ready(self):
        from functools import partial

        from django.apps import apps
        from django.db.models.signals import pre_delete

        from apps.shop import signals

        senders = [
            ("geo", "CountryModel", "country_id"),
            ("geo", "RegionModel", "region_id"),
            ("geo", "CityModel", "city_id"),
        ]

        for app_label, model_name, field_name in senders:
            Model = apps.get_model(app_label, model_name)
            pre_delete.connect(
                partial(signals.set_none_geo, field_name),
                sender=Model,
                dispatch_uid=f"shop.signals.set_none_geo_{model_name.lower()}",
            )
