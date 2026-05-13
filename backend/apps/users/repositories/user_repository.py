from apps.users.models import CustomUser
from apps.users.dto import RegisterDTO


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


user_repository = UserRepository()
