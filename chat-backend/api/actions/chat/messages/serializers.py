from api.models import Chat, Message, User
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username")
    owner = serializers.SerializerMethodField(method_name="is_owner")

    class Meta:
        # fields = "__all__"
        exclude = ["chat", "user"]
        model = Message

    def is_owner(self, obj):
        user_id = self.context["request"].user.id
        return True if user_id == obj.user_id else False
