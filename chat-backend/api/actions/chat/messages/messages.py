from api.actions.chat.messages.serializers import MessageSerializer
from api.models import Message
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination


class MessagesView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination
    serializer_class = MessageSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="chat_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        chat_id = self.request.query_params["chat_id"]
        queryset = Message.objects.filter(
            user=self.request.user, chat_id=chat_id
        )
        return queryset
