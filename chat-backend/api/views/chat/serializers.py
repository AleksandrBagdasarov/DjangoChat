from api.models import Chat
from rest_framework import serializers
from api.models import UserToChat
from api.models import Message


class ChatModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Chat


class MessageModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Message


class NewChatSerializer(ChatModelSerializer):
    owner = serializers.SerializerMethodField(method_name="get_owner")

    def get_owner(self):
        owner = self.context["request"].user
        return owner


class MessageReadOnlySerializer(MessageModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    owner = serializers.SerializerMethodField(method_name="is_owner")

    class Meta:
        fields = "__all__"
        model = Message
        read_only_fields = ['user', 'chat', 'username']

    def is_owner(self, obj):
        if "request" in self.context:
            user_id = self.context["request"].user.id
        elif "user_id" in self.context:
            user_id = self.context["user_id"]
        else:
            return False
        return True if user_id == obj.user_id else False


class ShowMyChatsSerializer(serializers.ModelSerializer):
    chat_name = serializers.CharField(source="chat.name")
    chat_owner = serializers.CharField(source="chat.owner.username")

    class Meta:
        model = UserToChat
        fields = "__all__"
