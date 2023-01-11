from api.actions.chat.show_chats.serializer import ShowMyChatsSerializer
from api.models import UserToChat
from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination


class ShowMyChatsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ShowMyChatsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = UserToChat.objects.filter(user=self.request.user)
        else:
            queryset = UserToChat.objects.filter(chat__name="Anonymous")
        return queryset
