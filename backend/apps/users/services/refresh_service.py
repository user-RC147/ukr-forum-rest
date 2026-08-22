from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.dto.login_in_dto import LoginOutDTO, _to_dto_login
from apps.users.models.user import CustomUser


class RefreshService:

    def refresh(self, refresh_token_str: str) -> LoginOutDTO:
        try:
            old_refresh = RefreshToken(refresh_token_str)
        except TokenError:
            raise ValueError("Токен оновлення недійсний або протух")

        # тут потрібно згенерувати нову пару і занести старий у блекліст
        user_id = old_refresh["user_id"]
        old_refresh.blacklist()
        user = CustomUser.objects.get(id=user_id)
        refresh = RefreshToken.for_user(user)
        dto = _to_dto_login(refresh)

        return dto
