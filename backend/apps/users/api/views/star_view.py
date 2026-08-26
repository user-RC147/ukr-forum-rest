from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import status

from apps.users.api import serializers
from core.users.csrf_permission import CsrfPermission

from apps.users.services.star_service import StarService
from apps.users.api.serializers.star_serializer import StarOutCerializer

from core.func_print import prt

class StarPageViewSet(ViewSet):

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny(),CsrfPermission()]
        return [AllowAny()]
        
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = StarService()

    
    def list(self,request):
        try:
            all_user = self._service.get_all_user()
            serialazer = StarOutCerializer(all_user,many=True)
            results =serialazer.data
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #return Response({'results':results},status=status.HTTP_200_OK)