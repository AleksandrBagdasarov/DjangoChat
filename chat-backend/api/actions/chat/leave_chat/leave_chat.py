from api.actions.chat.leave_chat.serializer import LeaveChatSerializer
from api.models import UserToChat
from rest_framework import generics, permissions


class LeaveChatView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LeaveChatSerializer

    def get_queryset(self):
        chat = self.request.query_params
        user = self.request.user
        queryset = UserToChat.objects.get(user=user, chat=chat)
        return queryset
