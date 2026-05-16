from rest_framework import serializers
from apps.household.models import Asset


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model=Asset
        fields=[
            'id',
            'name',
            'group',
            'address_line',
            'country_id',
            'region_id',
            'city_id',
        ]
        read_only_fields = ['id']