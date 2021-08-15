from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.exceptions import ValidationError, NotFound


class ArticleSerializer(serializers.Serializer):
    """Defines the represention of an ingested Article"""

    comments = serializers.IntegerField()
    likes = serializers.IntegerField()
    body = serializers.CharField()

    def to_representation(self, obj):
        return obj.get_value()
