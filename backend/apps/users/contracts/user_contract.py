from apps.users.dto.user import UserDTO
from apps.users.porotocols.user_protocol import UserProtocol
from apps.users.services.user_service import user_service


class UserContract:
    def __init__(self) -> None:
        self.service = user_service

    def get(self, user_id: int) -> UserDTO | None:
        return self.service.get_user(user_id)

    def get_many(self, ids: list[int]) -> list[UserDTO]:
        return self.service.get_users(ids)


def get_user_contract() -> UserProtocol:
    return UserContract()
