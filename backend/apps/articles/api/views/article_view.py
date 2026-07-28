from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_spectacular.utils import extend_schema

from apps.articles.api.serializers.article_serializer import ArticleOutSerializer
from apps.articles.services.article_service import ArticleService



class ArticleViewSet(ViewSet):


    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self._service = ArticleService()


    def list(self, request)->ArticleOutSerializer:
        user_id = request.user.id

        get_all_artcle = self._service.get_all_article(user_id)

        results = ArticleOutSerializer(get_all_artcle,many=True).data


        return Response({'results':True},status=status.HTTP_200_OK)

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