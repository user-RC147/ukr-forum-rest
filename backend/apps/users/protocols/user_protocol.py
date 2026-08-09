from typing import Protocol

from apps.users.dto.user_dto import UserShortOutDTO


class UserProtocol(Protocol):
    def get(self, user_id: int) -> UserShortOutDTO | None: ...
    def get_many(self, ids: list[int]) -> dict[int,UserShortOutDTO]: ...
