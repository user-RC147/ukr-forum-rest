# from django.apps import AppConfig


# class GeoConfig(AppConfig):
#     name = 'apps.geo'
#     verbose_name="Геолокація"


from django.apps import AppConfig


class GeoConfig(AppConfig):
    name = 'apps.geo'
    verbose_name = 'Локація(GEO)'

    # Публічна точка доступу до сервісу для інших модулів системи.
    # Вона типізується інтерфейсом-контрактом core.contracts.geo.IGeoServiceContract
    service = None

    def ready(self) -> None:
        """
        Метод викликається один раз, коли Django повністю завантажив додаток GEO.
        Тут ми ініціалізуємо репозиторій та сервіс.
        """
        # Імпортуємо класи шарів всередині ready(), щоб уникнути передчасного завантаження моделей
        from apps.geo.repositories.geo_repository import GeoRepository
        from apps.geo.services.geo_service import GeoService

        # 1. Створюємо єдиний екземпляр репозиторію (працює з БД)
        repository = GeoRepository()

        # 2. Створюємо сервіс і передаємо йому репозиторій як залежність.
        # Записуємо його в атрибут класу GeoConfig.
        GeoConfig.service = GeoService(repository=repository)