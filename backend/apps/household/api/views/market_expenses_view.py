from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.household.api.serializers.paginator_purchase_item_serializer import PaginatorSerializerOut
from apps.household.services.market_service import MarketService
from apps.household.api.serializers.market_serializer import MarketExpenseOutSerializer,MarketExpense_Id_OutSerializer




class MarketExpenseViewSet(ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._service = MarketService()

  
    
    def list(self, request):
        user_id = int(request.user.id)
        page=int(request.query_params.get('page',1))
        page_size=int(request.query_params.get('page_size',5))
        date_from=request.query_params.get('date_from')
        date_to=request.query_params.get('date_to')

        get_market_expenses = self._service.get_market_expenses(user_id, page, page_size,date_from,date_to)

        results = MarketExpense_Id_OutSerializer(get_market_expenses.items, many=True)  #MarketExpenseOutSerializer

        paginator = PaginatorSerializerOut(get_market_expenses)

        return Response({'results': results.data, 'paginator': paginator.data},status=status.HTTP_200_OK)

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
