# search/services.py
import logging

from .contracts import SearchResultItem
from .registry import SearchRegistry

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, limit_per_module: int = 10) -> None:
        self.limit_per_module = limit_per_module

    def search(self, params) -> list[SearchResultItem]:
        results: list[SearchResultItem] = []

        for name, handler in SearchRegistry.all().items():
            try:
                found = handler.search(params)
                results.extend(found)
            except Exception:
                # one errored module don`t drop all search
                logger.exception("Search failed in module: %s", name)

        return results
