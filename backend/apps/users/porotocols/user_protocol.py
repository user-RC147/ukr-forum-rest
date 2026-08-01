from typing import Protocol

from apps.users.dto.user_dto import UserDTO


class UserProtocol(Protocol):
    def get(self, user_id: int) -> UserDTO | None: ...
    def get_many(self, ids: list[int]) -> dict[int, UserDTO]: ...
