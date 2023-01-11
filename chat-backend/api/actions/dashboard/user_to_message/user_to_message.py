from api.actions.dashboard.user_to_message.serializer import (
    UserToMessageSerializer,
)
from api.models import Message
from django.db.models import Count
from rest_framework import generics, permissions


class UserToMessageView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserToMessageSerializer

    def get_queryset(self):
        chat_id = self.request.query_params
        queryset = (
            Message.objects.filter(chat_id=chat_id)
            .values("user")
            .annotate(message_quantity=Count("user"))
            .order_by("message_quantity")
        )
        return queryset
