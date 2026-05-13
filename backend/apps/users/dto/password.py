from dataclasses import dataclass


@dataclass
class PasswordResetConfirmDTO:
    uid: str
    token: str
    new_password: str


@dataclass
class ChangePasswordDTO:
    old_password: str
    new_password: str
    