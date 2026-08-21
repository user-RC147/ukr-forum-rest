from django.contrib import admin

from .models import CategoryModel, TagModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_per_page = 20
    ordering = ["name"]
    show_full_result_count = False
    readonly_fields = ["id"]


@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_per_page = 20
    ordering = ["name"]
    show_full_result_count = False
    readonly_fields = ["id"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")
