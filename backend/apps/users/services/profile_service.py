# apps/users/services/profile_service.py
from django.apps import apps
from apps.users.models import CustomUser
from apps.users.dto import ProfileUpdateDTO, LocationUpdateDTO
from apps.users.repositories.user_repository import user_repository
from apps.users.contracts.geo_contract import GeoServiceProtocol


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
        geo_svc: GeoServiceProtocol | None = None,  # ← Змінено за замовчуванням на None
        ) -> CustomUser:
    """
    Оновлює локацію користувача.
    users модуль зберігає тільки id — не FK об'єкти.
    """
    # Якщо geo_svc не передали вручну (наприклад, у тестах), 
    # беремо його з IoC-контейнера додатка geo ледачим способом
    if geo_svc is None:
        geo_svc = apps.get_app_config('geo').service

    user.country_id = dto.country_id
    user.region_id  = dto.region_id
    user.city_id    = dto.city_id

    # Приклад: якщо в майбутньому знадобиться викликати метод гео-сервісу
    # geo_svc.validate_location(dto.city_id)

    return user_repository.save(user)