from django.conf import settings
from django.utils.module_loading import import_string

from .contracts.protocols import Searchable


class SearchRegistry:
    _handlers: dict[str, Searchable] = {}

    @classmethod
    def load_from_settings(cls) -> None:
        paths: dict[str, str] = getattr(settings, "SEARCH_HANDLERS", {})

        for module_name, dotted_path in paths.items():
            handler_class = import_string(dotted_path)

            if not isinstance(handler_class(), Searchable):
                raise TypeError(f"{dotted_path} doesn`t have Searchable protocol")

            cls._handlers[module_name] = handler_class()

    @classmethod
    def all(cls) -> dict[str, Searchable]:
        return dict(cls._handlers)
