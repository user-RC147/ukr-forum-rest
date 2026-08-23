from collections.abc import Callable
import logging

from django.contrib import admin
from django.core.cache import cache

logger = logging.getLogger(__name__)


def invalidate_cache(key: str) -> None:
    """Cache delete with try block and logger inside"""
    try:
        cache.delete(key)
    except Exception:
        logger.exception(
            "Failed to invalidate cache",
            extra={"key": key, "event": "cache_invalidation"},
        )
    else:
        logger.debug(
            "Cache invalidated", extra={"key": key, "event": "cache_invalidation"}
        )


class CacheInvalidationAdminMixin(admin.ModelAdmin):
    """Require cache_key variable in admin class with str cache key"""

    cache_key: str

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        invalidate_cache(self.cache_key)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        invalidate_cache(self.cache_key)

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        invalidate_cache(self.cache_key)


class DynamicCacheInvalidationAdminMixin(admin.ModelAdmin):
    """
    Require cache_key_field and cache_key_builder(wrapped in staticmethod func) variables in admin class with str cache key
    """

    cache_key_field: str  # example: "country_id"
    cache_key_builder: Callable[[int], str]  # example: region_by_country_cache_key

    def _invalidate(self, obj) -> None:
        field_value = getattr(obj, self.cache_key_field)
        invalidate_cache(self.cache_key_builder(field_value))

    def save_model(self, request, obj, form, change):
        old_value = None
        if change:
            old_value = (
                self.model.objects.filter(pk=obj.pk)
                .values_list(self.cache_key_field, flat=True)
                .first()
            )

        super().save_model(request, obj, form, change)

        new_value = getattr(obj, self.cache_key_field)
        invalidate_cache(self.cache_key_builder(new_value))
        if old_value is not None and old_value != new_value:
            invalidate_cache(self.cache_key_builder(old_value))

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        self._invalidate(obj)

    def delete_queryset(self, request, queryset):
        field_values = set(queryset.values_list(self.cache_key_field, flat=True))
        super().delete_queryset(request, queryset)
        for value in field_values:
            invalidate_cache(self.cache_key_builder(value))
