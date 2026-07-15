import logging

from config.middleware import request_id_var, user_id_var


class DropNonSerializableFilter(logging.Filter):
    DROP_KEYS = ("request",)

    def filter(self, record: logging.LogRecord) -> bool:
        for key in self.DROP_KEYS:
            if hasattr(record, key):
                delattr(record, key)
        return True


class RequestIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True

class UserIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.user_id = user_id_var.get()
        return True