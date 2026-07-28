from rest_framework import serializers


class PageSerializerBase(serializers.Serializer):
    """Please, define items field in child classes
    (items = ur serializer)"""

    # items = *ur serializer*
    count = serializers.IntegerField()
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()
