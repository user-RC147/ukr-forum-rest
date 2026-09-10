import uuid
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


from apps.users.dto.user_dto import (
    PasswordResetTokenOutDTO,
    UserShortPublicOutDTO,
    CreateUserInDTO,
    UserPrivateOutDTO,
    UserShortOutDTO,
    UserPrivateUpdateInDTO,
    User_Id_PrivateOutDTO,
)
from apps.users.dto._to_dto_user import (
    _to_dto_user_in,
    _to_dto_public_id_user_out,
    _to_dto_public_user_out,
)
from apps.users.dto._to_dto_profile import _to_dto_id_location_profile

from apps.users.models import CustomUser, ReferralCode, ReferralUsage
from apps.users.models.password_reset_token import PasswordResetToken


class UserRepo:

    def create(self, dto: CreateUserInDTO, referral_code) -> UserShortPublicOutDTO:

        user = CustomUser.objects.create_user(
            username=dto.username,
            password=dto.password,
            display_name=dto.display_name,
            email=dto.email,
            consent_given=dto.consent_given,
            is_active=False,
        )

        if referral_code:
            ReferralUsage.objects.create(
                code=referral_code,
                used_by=user,
            )

        return UserShortPublicOutDTO(
            id=user.id,
            display_name=user.display_name,
        )

    def update_my_profile(
        self, dto: UserPrivateUpdateInDTO, user_id: int
    ) -> User_Id_PrivateOutDTO:

        user = CustomUser.objects.get(id=user_id)

        user.display_name = dto.display_name
        user.first_name = dto.first_name
        user.first_name_public = dto.first_name_public

        user.last_name = dto.last_name
        user.last_name_public = dto.last_name_public

        user.email = dto.email
        user.email_public = dto.email_public

        user.date_of_birth = dto.date_of_birth
        user.date_of_birth_public = dto.date_of_birth_public

        user.phone_number = dto.phone_number
        user.phone_public = dto.phone_public

        user.social_network = dto.social_network
        user.social_public = dto.social_public

        user.country_public = dto.country_public
        user.region_public = dto.region_public
        user.city_public = dto.city_public

        user.country_id = dto.location.country_id
        user.region_id = dto.location.region_id
        user.city_id = dto.location.city_id

        user.save()

        return _to_dto_id_location_profile(user)

    def delete_user(self, user_id: int) -> None:
        user = CustomUser.objects.get(id=user_id)

        user.is_active = False
        user.deletion_scheduled_at = timezone.now() + timedelta(days=30)
        user.save()

    def create_password_reset_token(self, user_id) -> PasswordResetTokenOutDTO:

        password_reset = PasswordResetToken.objects.create(
            user_id=user_id,
            token=uuid.uuid4(),
            expires_at=timezone.now()
            + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_TTL_MINUTES),
        )

        return PasswordResetTokenOutDTO(
            id=password_reset.id,
            user_id=password_reset.user_id,
            token=str(password_reset.token),
            created_at=password_reset.created_at,
            expires_at=password_reset.expires_at,
            is_used=password_reset.is_used,
        )

    def confirm_password_reset(self, user_id: int, token_id: int, new_password: str) -> None:
        user = CustomUser.objects.get(id=user_id)
        user.set_password(new_password)
        user.is_active = True
        user.save()

        PasswordResetToken.objects.filter(id=token_id).update(is_used=True)
