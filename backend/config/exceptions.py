import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    request = context.get("request")
    view = context.get("view")

    user_id = getattr(getattr(request, "user", None), "id", None)
    path = getattr(request, "path", None)
    method = getattr(request, "method", None)
    view_name = view.__class__.__name__ if view else None

    if response is not None:
        log_extra = {
            "user_id": user_id,
            "status_code": response.status_code,
            "path": path,
            "method": method,
            "view": view_name,
            "exception_type": type(exc).__name__,
        }
        if response.status_code >= 500:
            logger.error("Server error handled by DRF", extra=log_extra, exc_info=True)
        else:
            logger.warning("Client error", extra={**log_extra, "detail": response.data})
        return response

    logger.error(
        "Unhandled exception",
        extra={
            "user_id": user_id,
            "path": path,
            "method": method,
            "view": view_name,
            "exception_type": type(exc).__name__,
        },
        exc_info=True,
    )
    return Response({"detail": "Internal server error"}, status=500)
