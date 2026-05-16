# apps/users/services/profile_service.py
from apps.users.models import CustomUser
from apps.users.dto import ProfileUpdateDTO, LocationUpdateDTO
from apps.users.repositories.user_repository import user_repository
from apps.users.contracts.geo_contract import GeoServiceProtocol
from apps.geo.services.geo_service import geo_service


def update_profile(
        user: CustomUser,
        dto: ProfileUpdateDTO) -> CustomUser:
    """
    Оновлює тільки ті поля які були передані (не None).
    Зберігає в БД і повертає оновленого користувача.
    """
    for field, value in vars(dto).items():
        if value is not None:
            setattr(user, field, value)
    return user_repository.save(user)


def update_location(
        user: CustomUser,
        dto: LocationUpdateDTO,
        geo_svc: GeoServiceProtocol = geo_service,
        ) -> CustomUser:
    """
    Оновлює локацію користувача.
    users модуль зберігає тільки id — не FK об'єкти.
    """
    user.country_id = dto.country_id
    user.region_id  = dto.region_id
    user.city_id    = dto.city_id

    return user_repository.save(user)