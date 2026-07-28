# search/serializers.py
from rest_framework import serializers

from core.paginator.serializers import PageSerializerBase


class SearchResultItemSerializer(serializers.Serializer):
    resource_type = serializers.CharField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    meta = serializers.DictField()


class PageSerializer(PageSerializerBase):
    items = SearchResultItemSerializer(many=True)


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tags = serializers.DictField()


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
