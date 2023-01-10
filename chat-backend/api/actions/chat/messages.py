from api.actions.chat.serializers import MessageSerializer
from api.models import Chat, Message
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, response, status
from rest_framework.pagination import LimitOffsetPagination


class MessagesView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.filter(user=self.request.user)
        return queryset
