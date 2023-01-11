from rest_framework import serializers


class ChatToMessageByDateSerializer(serializers.Serializer):
    chat_name = serializers.CharField(max_length=100)
    chat_id = serializers.IntegerField()
    day = serializers.DateField()
    message_quantity = serializers.IntegerField()
