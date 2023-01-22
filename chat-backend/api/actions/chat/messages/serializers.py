from api.models import Message
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username")
    owner = serializers.SerializerMethodField(method_name="is_owner")

    class Meta:
        model = Message
        fields = "__all__"
        # read_only_fields = ['user']
        # extra_kwargs = {'user': {'read_only': True}}

    def is_owner(self, obj):
        if "request" in self.context:
            user_id = self.context["request"].user.id
        elif "user_id" in self.context:
            user_id = self.context["user_id"]
        else:
            return False
        return True if user_id == obj.user_id else False
