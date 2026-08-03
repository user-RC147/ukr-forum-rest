#login_in_dto.py
from dataclasses import dataclass


@dataclass(frozen=True)
class LoginOutDTO:
    access_token:str
    refresh_token:str


def _to_dto_login(data):
    return LoginOutDTO(
        access_token=str(data.access_token),
        refresh_token=str(data),
    )