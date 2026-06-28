from django.contrib import admin

from .models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["title", "description"]
    list_per_page = 25
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    show_full_result_count = False
    readonly_fields = ["id", "created_at"]
