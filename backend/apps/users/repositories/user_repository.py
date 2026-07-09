from django.db import transaction
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from apps.users.dto import RegisterDTO
from apps.users.models import CustomUser


class UserRepository:
    def create(self, dto: RegisterDTO) -> CustomUser:
        return CustomUser.objects.create_user(
            username=dto.username,
            email=dto.email,
            password=dto.password,
            country=dto.country,
            region=dto.region,
            city=dto.city,
        )

    def get_by_email(self, email: str) -> CustomUser | None:
        return CustomUser.objects.filter(email=email).first()

    def get_by_pk(self, pk) -> CustomUser | None:
        return CustomUser.objects.filter(pk=pk).first()

    def delete(self, user: CustomUser) -> None:
        user.delete()

    def save(self, user: CustomUser) -> CustomUser:
        user.save()
        return user

    def to_blacklist_tokens(self, user_id: int):
        user = self.get_by_pk(user_id)
        tokens = OutstandingToken.objects.filter(user=user)

        with transaction.atomic():
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)


user_repository = UserRepository()
