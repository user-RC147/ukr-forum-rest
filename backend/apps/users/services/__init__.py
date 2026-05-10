# apps/users/services/__init__.py
from .auth_service import auth_service
from .profile_service import get_profile, update_profile, update_location
from .consent_service import give_consent, revoke_consent

__all__ = [
    # auth
    "auth_service",

    # profile
    "get_profile",
    "update_profile",
    "update_location",

    # consent
    "give_consent",
    "revoke_consent",
]