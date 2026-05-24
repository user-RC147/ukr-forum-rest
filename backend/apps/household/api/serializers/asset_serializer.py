from rest_framework import serializers

class AssetSerializer(serializers.Serializer):

    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(read_only=True)
    address_line=serializers.CharField(read_only=True)
    group_name=serializers.CharField(source='group.name',read_only=True)