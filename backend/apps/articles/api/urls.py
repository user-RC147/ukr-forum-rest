from rest_framework.routers import DefaultRouter

from apps.articles.api.views.article_view import ArticleViewSet



router = DefaultRouter()

router.register('articles',ArticleViewSet, basename='article')


urlpatterns = router.urls
