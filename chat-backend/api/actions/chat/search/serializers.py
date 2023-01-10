from api.models import Chat
from rest_framework import serializers


class ChatByNameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Chat
