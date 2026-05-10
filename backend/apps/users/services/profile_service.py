# apps/users/services/profile_service.py
from apps.users.models import CustomUser
from apps.users.dto import ProfileUpdateDTO, LocationUpdateDTO
from apps.geo.services.geo_db_service import (
    get_or_create_country,
    get_or_create_region,
    get_or_create_city,
)
from apps.geo.services.geo_service import geo_service


def get_profile(user: CustomUser) -> CustomUser:
    """
    Повертає профіль користувача.
    
    Поки просто повертає об'єкт — але в майбутньому тут може бути:
    - перевірка чи не заблокований акаунт
    - підрахунок статистики
    - кешування
    Тому виносимо в сервіс вже зараз, а не в view.
    """
    return user


def update_profile(user: CustomUser, dto: ProfileUpdateDTO) -> CustomUser:
    """
    Оновлює тільки ті поля які були передані (не None).
    Зберігає в БД і повертає оновленого користувача.
    """
    # vars(dto) перетворює dataclass в словник:
    # ProfileUpdateDTO(display_name="Іван", age=None, phone_number=None ...)
    # → {"display_name": "Іван", "age": None, "phone_number": None ...}
    
    for field, value in vars(dto).items():
        if value is not None:           # пропускаємо поля які не передали
            setattr(user, field, value) # user.display_name = "Іван"

    user.save()
    return user

def update_location(user: CustomUser, dto: LocationUpdateDTO) -> CustomUser:
    user.country = None
    user.region  = None
    user.city    = None

    if dto.country_id:
        countries    = geo_service.get_countries()
        # countries — це список [], не словник з results
        country_data = next(
            (c for c in countries if c['id'] == dto.country_id),  # ← прибрали ['results']
            None
        )
        if country_data:
            user.country = get_or_create_country(country_data)

    if dto.region_id and user.country:
        regions     = geo_service.get_regions(country_code=user.country.code)
        region_data = next(
            (r for r in regions['results'] if r['id'] == dto.region_id),  # ← regions має results
            None
        )
        if region_data:
            user.region = get_or_create_region(region_data, user.country)

    if dto.city_id and user.region:
        cities    = geo_service.get_cities(region_id=dto.region_id)
        city_data = next(
            (c for c in cities['results'] if c['id'] == dto.city_id),  # ← cities теж перевіримо
            None
        )
        if city_data:
            user.city = get_or_create_city(city_data, user.country, user.region)

    user.save()
    return user