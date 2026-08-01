from apps.users.models.user import CustomUser
from apps.users.dto.user_dto import UserOutDTO


class UserSelector:

    def get_all_users(self) -> list[UserOutDTO]:

        users = CustomUser.objects.all()

        dto = [_to_dto_user(user) for user in users]

        return dto

    def get_user_by_id(self, user_id: int) -> UserOutDTO:

        user = CustomUser.objects.get(id=user_id)

        dto = _to_dto_user(user)

        return dto


def _to_dto_user(data) -> UserOutDTO:
    return UserOutDTO(
        id=data.id,
        username=data.username,
        display_name=data.display_name
    )
