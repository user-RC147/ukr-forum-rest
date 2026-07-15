from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.middleware import user_id_var


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        cookie_name = settings.SIMPLE_JWT["AUTH_COOKIE"]
        raw_token = request.COOKIES.get(cookie_name)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        self._enforce_csrf_if_needed(request)

        user_id_var.set(user.id)

        return user, validated_token

    def _enforce_csrf_if_needed(self, request):
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            self.enforce_csrf(request)

    def enforce_csrf(self, request):
        def dummy_get_response(request):
            return None

        check = CsrfViewMiddleware(dummy_get_response)
        result = check.process_view(request, None, (), {})

        if result is not None:
            raise exceptions.PermissionDenied(
                "CSRF Failed: CSRF token missing or incorrect."
            )
