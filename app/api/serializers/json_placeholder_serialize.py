from rest_framework import serializers


class JsonPlaceholderSerializer(serializers.Serializer):
    id: serializers.IntegerField()
    title: serializers.CharField()
