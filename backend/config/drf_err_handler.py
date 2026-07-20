import logging

from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .exceptions import (
    AppError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
)
from .exceptions import (
    ValidationError as AppValidationError,
)

logger = logging.getLogger(__name__)

EXPECTED_AUTH_NOISE = (NotAuthenticated, InvalidToken, TokenError)

APP_ERROR_STATUS_MAP = (
    (AppValidationError, status.HTTP_400_BAD_REQUEST),
    (PermissionDeniedError, status.HTTP_403_FORBIDDEN),
    (NotFoundError, status.HTTP_404_NOT_FOUND),
    (ConflictError, status.HTTP_409_CONFLICT),
)


def _build_app_error_response(exc: AppError) -> Response:
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    for exc_type, code in APP_ERROR_STATUS_MAP:
        if isinstance(exc, exc_type):
            status_code = code
            break

    payload = {"detail": exc.message, "code": exc.code}
    if isinstance(exc, AppValidationError) and exc.errors:
        payload["errors"] = exc.errors

    return Response(payload, status=status_code)


def custom_exception_handler(exc, context):
    request = context.get("request")
    view = context.get("view")

    user_id = getattr(getattr(request, "user", None), "id", None)
    path = getattr(request, "path", None)
    method = getattr(request, "method", None)
    view_name = view.__class__.__name__ if view else None

    # AppError
    if isinstance(exc, AppError):
        response = _build_app_error_response(exc)
    else:
        response = drf_exception_handler(exc, context)

    if response is not None:
        log_extra = {
            "user_id": user_id,
            "status_code": response.status_code,
            "path": path,
            "method": method,
            "view": view_name,
            "exception_type": type(exc).__name__,
            **getattr(
                exc, "extra", {}
            ),  # <-- context from raise
        }
        if response.status_code >= 500:
            logger.error("Server error handled by DRF", extra=log_extra, exc_info=True)
        elif isinstance(exc, EXPECTED_AUTH_NOISE):
            logger.info("Expected auth failure (token refresh flow)", extra=log_extra)
        elif isinstance(exc, AppError):
            logger.warning(
                f"Application error: {exc.code}",
                extra={**log_extra, "error_message": exc.message},
            )
        else:
            logger.warning(
                "Client error",
                extra={**log_extra, "detail": _sanitize_errors(response.data)},
            )
        return response

    logger.error(
        "Unhandled exception",
        extra={
            "user_id": user_id,
            "status_code": 500,
            "path": path,
            "method": method,
            "view": view_name,
            "exception_type": type(exc).__name__,
        },
        exc_info=True,
    )
    return Response({"detail": "Internal server error"}, status=500)


SENSITIVE_FIELD_NAMES = {
    "password",
    "password1",
    "password2",
    "new_password",
    "old_password",
    "token",
    "access",
    "refresh",
    "secret",
    "api_key",
    "card_number",
    "cvv",
    "ssn",
}


def _sanitize_errors(data):
    """Delete privat client info in DRF error payload."""
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            if str(key).lower() in SENSITIVE_FIELD_NAMES:
                sanitized[key] = (
                    f"<{len(value)} error(s) redacted>"
                    if isinstance(value, list)
                    else "<redacted>"
                )
            else:
                sanitized[key] = _sanitize_errors(value)
        return sanitized
    if isinstance(data, list):
        return [_sanitize_errors(item) for item in data]
    return data
