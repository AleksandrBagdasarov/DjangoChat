from api.models import UserToChat
from rest_framework import serializers


class ShowMyChatsSerializer(serializers.ModelSerializer):
    chat_name = serializers.CharField(source="chat.name")
    chat_owner = serializers.CharField(source="chat.owner.username")

    class Meta:
        model = UserToChat
        fields = "__all__"
