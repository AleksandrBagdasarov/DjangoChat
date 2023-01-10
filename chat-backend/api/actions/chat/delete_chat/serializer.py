from api.models import Chat
from rest_framework import serializers


class DeleteChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
