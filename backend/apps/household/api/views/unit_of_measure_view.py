from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.household.services.unit_of_measure_service import UnitOfMeasureService
from apps.household.api.serializers.unit_of_measure_serializer import UnitOfMeasureSerializer
from apps.household.dto.unit_of_measure_dto import CreateUnitOfMeasureInDTO



class UnitOfMeasureViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._service = UnitOfMeasureService()
        self._serializer = UnitOfMeasureSerializer
        


    def list(self, request):
        units = self._service.get_all_units()
        serializer = self._serializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
             
        

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