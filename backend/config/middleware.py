# config/middleware.py
import contextvars
import uuid

request_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)
user_id_var: contextvars.ContextVar[int | None] = contextvars.ContextVar(
    "user_id", default=None
)


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        rid_token = request_id_var.set(request_id)
        uid_token = user_id_var.set(None)
        request.request_id = request_id
        try:
            response = self.get_response(request)
        finally:
            request_id_var.reset(rid_token)
            user_id_var.reset(uid_token)
        response["X-Request-ID"] = request_id
        return response
