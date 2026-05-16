from typing import Protocol


class UserProtocol(Protocol):
    """
    Контракт для користувача.
    household не знає про users модуль напряму.
    """
    id:int
    username:str
    email:str
    display_name: str   # ← публічне ім'я для відображення в групі
    is_active: bool     # ← чи активний акаунт (не заблокований)