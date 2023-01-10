from api.models import Chat
from rest_framework import serializers


class NewChatSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(method_name="get_owner")

    class Meta:
        fields = "__all__"
        model = Chat

    def get_owner(self):
        owner = self.context["request"].user
        return owner
