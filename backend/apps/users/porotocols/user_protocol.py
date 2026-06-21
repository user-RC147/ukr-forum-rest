from typing import Protocol

from apps.users.dto.user import UserDTO


class UserProtocol(Protocol):
    def get(self, user_id: int) -> UserDTO: ...
    def get_many(self, ids: list[int]) -> dict[int, UserDTO]: ...
