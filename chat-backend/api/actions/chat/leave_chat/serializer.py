from api.models import UserToChat
from rest_framework import serializers


class LeaveChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToChat
