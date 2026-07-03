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
            ("geo", "Country", "country_id"),
            ("geo", "Region", "region_id"),
            ("geo", "City", "city_id"),
        ]

        for app_label, model_name, field_name in senders:
            Model = apps.get_model(app_label, model_name)
            pre_delete.connect(
                partial(signals.set_none_geo, field_name),
                sender=Model,
                dispatch_uid=f"shop.signals.set_none_geo_{model_name.lower()}",
            )
