from api.actions.chat.delete_chat.serializer import DeleteChatSerializer
from api.models import Chat
from rest_framework import generics, permissions


class DeleteChatView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeleteChatSerializer

    def get_queryset(self):
        chat_id = self.request.query_params
        user = self.request.user
        queryset = Chat.objects.get(id=chat_id, owner=user)
        return queryset
