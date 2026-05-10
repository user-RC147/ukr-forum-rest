# apps/users/dto.py
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RegisterDTO:
    """
    Дані для реєстрації нового користувача.
    Серіалізатор валідував їх — тут вже чисті дані.
    """
    username: str
    email: str
    password: str                   # вже перевірений, але ще не хешований
    country: Optional[str] = None  # необов'язкові поля мають default = None
    region: Optional[str] = None
    city: Optional[str] = None


@dataclass
class ProfileUpdateDTO:
    """
    Дані для оновлення профілю.
    Всі поля Optional — користувач може оновити тільки частину.
    """
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None
    social_network: Optional[str] = None
    consent_given: Optional[bool] = None


@dataclass
class PasswordResetConfirmDTO:
    """
    Дані для підтвердження відновлення паролю.
    uid і token приходять з URL посилання яке було в email.
    """
    uid: str            # закодований id користувача
    token: str          # токен з URL
    new_password: str   # новий пароль який хоче встановити користувач


@dataclass  
class ChangePasswordDTO:
    """
    Дані для зміни паролю коли користувач знає старий пароль.
    """
    old_password: str
    new_password: str


@dataclass
class LocationUpdateDTO:
    """
    Дані для оновлення локації користувача.
    Містить id з зовнішнього Geo API.
    """
    country_id: Optional[int] = None
    region_id:  Optional[int] = None
    city_id:    Optional[int] = None