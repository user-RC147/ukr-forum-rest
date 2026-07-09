import code
from rest_framework import serializers


class UnitOfMeasureSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code=serializers.CharField()
    name = serializers.CharField()
    