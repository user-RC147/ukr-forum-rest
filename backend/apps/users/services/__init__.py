# apps/users/services/__init__.py
from .auth_service import auth_service
from .profile_service import update_profile, update_location
from .consent_service import give_consent, revoke_consent
from .user_service  import UserService, user_service
from .profile_service import  update_profile,update_location

__all__ = [
    # auth
    "auth_service",

    # profile
    "update_profile",
    "update_location",
    'UserService',
    'user_service',

    # consent
    "give_consent",
    "revoke_consent",
]