# search/services.py
import logging

from .contracts import SearchResultItem
from .registry import SearchRegistry

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, limit_per_module: int = 10) -> None:
        self.limit_per_module = limit_per_module

    def search(self, params, scope: str | None = None) -> list[SearchResultItem]:
        handlers = SearchRegistry.all()
        items = handlers.items() if scope is None else [(scope, handlers[scope])]

        results: list[SearchResultItem] = []
        for name, handler in items:
            try:
                results.extend(handler.search(params))
            except Exception:
                logger.exception("Search failed in module: %s", name)
                if scope is not None:
                    raise

        return results
