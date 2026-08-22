from rest_framework.permissions import BasePermission

from core.users.csrf import CsrfEnforcer

_UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class CsrfPermission(BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method not in _UNSAFE_METHODS:
            return True

        CsrfEnforcer().enforce(request)
        return True