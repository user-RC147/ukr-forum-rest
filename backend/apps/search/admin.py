from django.contrib import admin

from core.cache.cache_invalidation import CacheInvalidationAdminMixin

from .models import CategoryModel, TagModel
from .repository import CATEGORY_CACHE_KEY, TAG_CACHE_KEY


@admin.register(CategoryModel)
class CategoryModelAdmin(CacheInvalidationAdminMixin, admin.ModelAdmin):
    cache_key = CATEGORY_CACHE_KEY
    search_fields = ["name"]
    list_per_page = 20
    ordering = ["name"]
    show_full_result_count = False
    readonly_fields = ["id"]


@admin.register(TagModel)
class TagModelAdmin(CacheInvalidationAdminMixin, admin.ModelAdmin):
    tag_key = TAG_CACHE_KEY
    search_fields = ["name"]
    list_per_page = 20
    ordering = ["name"]
    show_full_result_count = False
    readonly_fields = ["id"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")
