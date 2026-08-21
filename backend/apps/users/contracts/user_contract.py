from core.dto.users.user_dto import UserFullOutDTO, UserShortOutDTO

from apps.users.protocols.user_protocol import UserProtocol,UserShortProtocol
from apps.users.services.user_service import UserService  


class UserShortContract:
    def __init__(self) -> None:
        self._service = UserService()

    def get(self, user_id: int) -> UserShortOutDTO:
        return self._service.get_user_by_id(user_id)

    def get_many(self, ids: list[int]) -> dict[int,UserShortOutDTO]:
        return self._service.get_many(ids)


def get_user_short_contract() -> UserShortProtocol:
    return UserShortContract()


class UserContract:
    def __init__(self) -> None:
        self._service = UserService()

    def get(self, user_id: int) -> UserFullOutDTO():
        return self._service.get_user_by_id(user_id)

    def get_many(self, ids: list[int]) -> dict[int,UserFullOutDTO]:
        return self._service.get_many(ids)

def get_user_contract() -> UserProtocol:
    return UserContract()