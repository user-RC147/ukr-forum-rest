
from rest_framework.viewsets import ViewSet

from rest_framework.response import Response
from rest_framework import status

from apps.household.services.category_service import CategoryService
from apps.household.api.serializers.category_serializer import CategoryInSerializer





class CategoryViewSet(ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._repository=CategoryService()


    
    def list(self, request):
        categories = self._repository.get_all_category()
        serializer = CategoryInSerializer(categories,many=True)
        if serializer.is_valid:
            return Response(serializer.data,status=status.HTTP_200_OK)

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass