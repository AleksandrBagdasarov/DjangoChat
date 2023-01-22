from api.actions.chat.delete_chat.serializer import DeleteChatSerializer
from api.models import Chat, Message, UserToChat
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from api.views.chat.serializers import ChatModelSerializer, MessageReadOnlySerializer, MessageModelSerializer
from api.custom_permisson import IsOwner
from rest_framework.decorators import action


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatModelSerializer

    def get_queryset(self):
        if self.action == 'list':
            queryset = Chat.objects.filter(usertochat__user=self.request.user)
        elif self.action in ('message__create__list', 'message__partial_update__destroy'):
            queryset = Message.objects.filter(user=self.request.user, chat_id=self.kwargs.get('pk'))
        else:
            queryset = Chat.objects.all()
        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.action == 'message__create__list':
            if self.request.method == 'POST':
                serializer = MessageModelSerializer(*args, **kwargs)
            else:
                serializer = MessageReadOnlySerializer(*args, **kwargs)
        elif self.action == 'message__partial_update__destroy':
            serializer = MessageReadOnlySerializer(*args, **kwargs)
        else:
            serializer = super().get_serializer(*args, **kwargs)
        
        return serializer

    @swagger_auto_schema(
        method="get",
        responses={
            status.HTTP_200_OK: MessageReadOnlySerializer(many=True)
        }
    )
    @swagger_auto_schema(
        method="post",
        responses={
            status.HTTP_200_OK: MessageReadOnlySerializer()
        },
        request_body=MessageReadOnlySerializer()
    )
    @action(methods=["get", "post"], url_path="message", detail=True)
    def message__create__list(self, request, pk):
        if request.method == 'POST':
            data = request.data
            data.update({"chat": pk})
            serializer = self.get_serializer(data=data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            read_only_serializer = MessageReadOnlySerializer(instance, context={"request": request})
            return Response(read_only_serializer.data)
        else:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(
        method="patch",
        responses={
            status.HTTP_200_OK: MessageReadOnlySerializer()
        },
        request_body=MessageReadOnlySerializer()
    )
    @swagger_auto_schema(
        method="delete",
        responses={
            status.HTTP_204_NO_CONTENT: ""
        },
    )
    @action(methods=["patch", "delete"], url_path="message/<int:message_id>/", detail=True)
    def message__partial_update__destroy(self, request, pk, message_id):
        queryset = Message.objects.get(id=message_id)
        serializer = MessageReadOnlySerializer(queryset)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permissions_map = {
            'list': [permissions.IsAuthenticated],
            'create': [permissions.IsAuthenticated],
            'retrieve': [permissions.IsAuthenticated],
            'update': [permissions.IsAuthenticated, IsOwner],
            'partial_update': [permissions.IsAuthenticated, IsOwner],
            'destroy': [permissions.IsAuthenticated, IsOwner],

            'message_list': [permissions.IsAuthenticated, IsOwner],
            'message_partial_update': [permissions.IsAuthenticated, IsOwner],
        }

        permission_classes = permissions_map.get(self.action, [permissions.IsAuthenticated])
        return [permission() for permission in permission_classes]
