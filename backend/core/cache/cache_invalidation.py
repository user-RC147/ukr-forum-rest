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
    """Require tag_key variable in admin class with str cache key"""

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
