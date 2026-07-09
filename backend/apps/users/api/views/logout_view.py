import logging
from typing import Any

from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.services.auth_service import auth_service

logger = logging.getLogger(__name__)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = auth_service

    def post(self, request, *args, **kwargs):
        response = Response({"status": "OK"}, status=200)
        user_id = request.user.id

        if request.data.get("all"):
            self.service.to_blacklist_tokens(user_id)
            logger.info(
                "All refresh tokens blacklisted",
                extra={"user_id": user_id, "event": "logout_all"},
            )
            response.data = {"status": "All refresh tokens blacklisted"}
        else:
            refresh_token = request.COOKIES.get(
                settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"]
            ) or request.data.get("refresh_token")
            if not refresh_token:
                logger.warning(
                    "Refresh token not provided",
                    extra={"user_id": user_id, "event": "logout_failed"},
                )
                return Response({"detail": "Refresh token not provided"}, status=400)
            try:
                RefreshToken(token=refresh_token).blacklist()
            except TokenError:
                logger.warning(
                    "Invalid or expired refresh token",
                    extra={"user_id": user_id, "event": "logout_failed"},
                )
                return Response(
                    {"detail": "Invalid or expired refresh token"}, status=400
                )
            logger.info(
                "User logged out",
                extra={"user_id": user_id, "event": "logout"},
            )

        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        return response
