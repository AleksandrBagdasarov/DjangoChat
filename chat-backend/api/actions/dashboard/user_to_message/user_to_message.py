from api.actions.dashboard.user_to_message.serializer import (
    UserToMessageSerializer,
)
from api.models import Message
from django.db.models import Count, F
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions


class UserToMessageView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserToMessageSerializer

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
        queryset = (
            Message.objects.filter(chat_id=chat_id)
            .annotate(username=F("user__username"))
            .annotate(message_quantity=Count("user"))
            .values("username", "message_quantity")
            .order_by("message_quantity")
        )
        return queryset
