from django.contrib import admin

from .models import CategoryModel, TagModel

# Register your models here.


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    pass
