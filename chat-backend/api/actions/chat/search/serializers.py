from api.models import Chat
from rest_framework import serializers


class NameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)


class ChatByNameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Chat
