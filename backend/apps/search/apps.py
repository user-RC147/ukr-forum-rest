from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = "apps.search"
    verbose_name = "Пошук"

    def ready(self) -> None:
        from .registry import SearchRegistry

        SearchRegistry.load_from_settings()
