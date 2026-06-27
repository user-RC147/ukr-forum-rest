from .logout_view import LogoutView
from .views import (
    RegisterView,
    ProfileView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    DeleteAccountView,
    LocationUpdateView, 
    )

__all__ = [
    'LogoutView',
    'RegisterView',
    'ProfileView',
    'ChangePasswordView',
    'PasswordResetRequestView',
    'PasswordResetConfirmView',
    'DeleteAccountView',
    'LocationUpdateView'
]