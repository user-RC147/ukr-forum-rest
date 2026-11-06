from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class CsrfViewSet(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        get_token(request)
        return Response({"detail": "CSRF cookie set"})
