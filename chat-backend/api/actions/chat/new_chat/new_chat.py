from api.actions.chat.new_chat.serializer import NewChatSerializer
from api.models import Chat
from rest_framework import generics, permissions


class NewChatView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = NewChatSerializer
