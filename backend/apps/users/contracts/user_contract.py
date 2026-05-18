from typing import Protocol, Optional
from apps.users.dto.user import UserDTO


class UserServiceProtocol(Protocol):
    """
    Контракт публічного сервісу users.
    Інші модулі залежать від цього протоколу, не від реалізації.
    """
    def get_user(self, user_id: int) -> Optional[UserDTO]: ...
    def get_users(self, ids: list[int]) -> list[UserDTO]: ...