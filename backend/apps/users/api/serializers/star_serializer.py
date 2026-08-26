from rest_framework import serializers

from core.serializers.location_serializer import Location_id_region_OutSerializer


class StarOutCerializer(serializers.Serializer):
    id=serializers.IntegerField()
    location=Location_id_region_OutSerializer()