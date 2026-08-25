from .user_view import UserViewSet
from .refresh_view import RefreshViewSet
from .csrf_view import CsrfViewSet
from.login_view import LoginViewSet
from .password_reset_view import PasswordResetViewSet
from .logout_view import LogoutViewSet
from .star_view import StarPageViewSet

__all__ = [
    'UserViewSet',
    'RefreshViewSet',
    'CsrfViewSet',
    'LoginViewSet',
    'PasswordResetViewSet',
    'LogoutViewSet',
    'StarPageViewSet'
    ]