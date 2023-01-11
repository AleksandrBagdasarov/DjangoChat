from api.actions.chat.delete_chat.serializer import DeleteChatSerializer
from api.models import Chat
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions


class DeleteChatView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeleteChatSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="chat_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        chat_id = self.request.query_params["chat_id"]
        user = self.request.user
        queryset = Chat.objects.get(id=chat_id, owner=user)
        return queryset
