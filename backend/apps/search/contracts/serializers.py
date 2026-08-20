from rest_framework import serializers


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tags = TagSerializer(many=True)
