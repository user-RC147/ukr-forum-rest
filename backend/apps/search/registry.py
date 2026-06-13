from django.conf import settings
from django.utils.module_loading import import_string

from .contracts import Searchable


class SearchRegistry:
    _handlers: dict[str, Searchable] = {}

    @classmethod
    def load_from_settings(cls) -> None:
        paths: list[str] = getattr(settings, "SEARCH_HANDLERS", [])

        for dotted_path in paths:
            handler_class = import_string(dotted_path)  # import class by strings
            handler = handler_class()

            if not isinstance(handler, Searchable):
                raise TypeError(f"{dotted_path} doesn`t have Searchable protocol")

            # key = first part of path, name of module ("shop", "users")
            module_name = dotted_path.split(".")[0]
            cls._handlers[module_name] = handler

    @classmethod
    def all(cls) -> dict[str, Searchable]:
        return dict(cls._handlers)
