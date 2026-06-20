from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.conf import settings




class LogoutView(APIView):
    """
    POST /api/users/logout/
    Видаляє cookies (очищує сесію користувача).
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # 1. Створи response
        response = Response(
            {"detail": "Успішно розлоговані."},
            status=status.HTTP_200_OK,
        )
        
        # 2. Видали cookies
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        
        # 3. Повернули response
        return response