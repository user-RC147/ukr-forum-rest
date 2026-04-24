from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,      # генерує schema.yml
    SpectacularSwaggerView,  # Swagger UI — зручний інтерфейс для тестування API
)

from django.conf import settings




urlpatterns = [
    path('admin/', admin.site.urls),

    # Всі ендпоінти users під префіксом /api/users/
    path('api/users/', include('apps.users.urls')),

    # OpenAPI документація — відкрий http://localhost:8000/api/docs/
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# debug toolbar тільки в режимі розробки
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]