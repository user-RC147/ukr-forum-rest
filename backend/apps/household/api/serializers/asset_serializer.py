from rest_framework import serializers

class AssetSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()          # ← приймає дані
    group = serializers.IntegerField(write_only=True)  # ← тільки для запису
    group_id = serializers.IntegerField(read_only=True)  # ← для читання
    address_line = serializers.CharField(required=False, allow_null=True)
    group_name = serializers.CharField(source='group.name', read_only=True)



class AssetListFilterSerializer(serializers.Serializer):
    # Тепер параметр можна не передавати
    group_id = serializers.IntegerField(required=False, allow_null=True)