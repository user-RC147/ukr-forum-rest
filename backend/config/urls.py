from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,  # генерує schema.yml
    SpectacularSwaggerView,  # Swagger UI — зручний інтерфейс для тестування API
)
from rest_framework_simplejwt.views import TokenBlacklistView
from .views import HealthView
urlpatterns = [
    path("admin/", admin.site.urls),
    # Всі ендпоінти users під префіксом /api/users/
    # Users
    path("api/users/", include("apps.users.api.urls")),
    path("api/auth/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # Geo
    path("api/geo/", include("apps.geo.api.urls")),
    path("api/household/", include("apps.household.api.urls")),
    # Shop
    path("api/shop/", include("apps.shop.urls")),
    # Search
    path("api/search/", include("apps.search.urls")),
    # Health endpoints
    path("health/", HealthView.as_view(), name="health_check"),
    # OpenAPI документація — відкрий http://localhost:8000/api/docs/
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# rest framework
urlpatterns += [
    # URLs specific omly to Django REST Framework:
    path("api-auth/", include("rest_framework.urls")),
]

# debug toolbar тільки в режимі розробки
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
