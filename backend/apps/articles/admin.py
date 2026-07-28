from django.contrib import admin

from apps.articles.models.article_model import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "created_by",
        "date_create",
        "date_edit",
    )
