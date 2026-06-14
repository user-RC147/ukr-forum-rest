from django.apps import AppConfig


class GeoConfig(AppConfig):
    name = 'apps.geo'
    verbose_name = 'Локація(GEO)'

    # Внутрішня кеш-змінна для Singleton-об'єкта сервісу
    _service = None

    @property
    def service(self):
        """
        Ледача ініціалізація сервісу GEO.
        Об'єкт створюється лише тоді, коли до нього вперше звертаються.
        """
        if self._service is None:
            # Імпортуємо класи шарів всередині property, щоб уникнути 
            # передчасного завантаження моделей та циклічних імпортів
            from apps.geo.repositories.geo_repository import GeoRepository
            from apps.geo.services.geo_service import GeoService

            # 1. Створюємо екземпляр репозиторію
            repository = GeoRepository()

            # 2. Збираємо сервіс, передаючи йому репозиторій як залежність
            self._service = GeoService(repository=repository)
            
        return self._service