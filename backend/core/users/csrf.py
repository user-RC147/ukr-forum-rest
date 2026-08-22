from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.exceptions import PermissionDenied


class CsrfEnforcer:

    def enforce(self, request) -> None:
        check = CsrfViewMiddleware(lambda r: None)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise PermissionDenied(f"CSRF помилка: {reason}")