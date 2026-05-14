
from shutil import ExecError


class GeoApiTimeoutError(Exception):
    """Зовнішній Geo API не відповідає."""
    default_message="Geo API не відповідає (timeout)."

    def __init__(self, message: str=None):
        self.message=message or self.default_message
        super().__init__(self.message)




class GeoApiError(Exception):
    """Загальна помилка зовнішнього Geo API."""
    default_message = "Помилка Geo API."

    def __init__(self, message: str = None):
        self.message = message or self.default_message
        super().__init__(self.message)