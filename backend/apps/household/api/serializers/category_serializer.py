from rest_framework import serializers



class CategoryInSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(max_length=100)
    icon=serializers.CharField(max_length=10, required=False, allow_blank=True, default="")
    is_active=serializers.BooleanField(required=False, default=True)
    parent_id=serializers.IntegerField(required=False, allow_null=True)