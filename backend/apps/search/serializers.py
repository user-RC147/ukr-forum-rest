# search/serializers.py
from rest_framework import serializers


class SearchResultItemSerializer(serializers.Serializer):
    resource_type = serializers.CharField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    meta = serializers.DictField()


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tags = serializers.DictField()

class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
