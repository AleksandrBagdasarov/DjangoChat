from api.models import Message, UserToChat
from rest_framework import serializers


class UserToMessageSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    message_quantity = serializers.IntegerField()
