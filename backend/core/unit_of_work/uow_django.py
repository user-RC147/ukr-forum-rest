from django.db import transaction

from .uow import UnitOfWork


class DjangoUnitOfWork(UnitOfWork):
    def __enter__(self):
        self._atomic = transaction.atomic()
        return self._atomic.__enter__()

    def __exit__(self, exc_type, exc, tb) -> bool | None:
        return self._atomic.__exit__(exc_type, exc, tb)

    def on_commit(self, callback) -> None:
        transaction.on_commit(callback)
