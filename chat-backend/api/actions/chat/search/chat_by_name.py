from api.actions.chat.search.serializers import (
    ChatByNameSerializer,
    NameSerializer,
)
from api.models import Chat
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions


class ChatByNameView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ChatByNameSerializer

    def get_queryset(self):
        query_name = self.request.query_params
        queryset = Chat.objects.filter(name__icontains=query_name)
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="chat_name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
