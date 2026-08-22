import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.shop.service import get_service

logger = logging.getLogger("shop")

User = get_user_model()


@receiver(pre_delete, sender=User)
def delete_owned_products(sender, instance, **kwargs):
    service = get_service()
    deleted_count = service.delete_all_by_user(instance.id)
    logger.info("Deleted %s products for user id=%s", deleted_count, instance.id)


def set_none_geo(field_name, sender, instance, **kwargs):
    service = get_service()

    products = service.nullify_geo(field_name, instance.pk)

    logger.critical(
        "Deleted from model:%s, geo data id:%s, object name:%s. Some products could be unstable, changed %s products!",
        instance.__class__.__name__,
        instance.pk,
        instance,
        products,
    )
