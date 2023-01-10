from api.actions.auth import UserBasicAuthView
from api.actions.chat import (
    DeleteChatView,
    LeaveChatView,
    MessagesView,
    NewChatView,
)
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # chat/
    path("chat", NewChatView.as_view(), name="new_chat"),
    path(
        "chat/<str:chat_id>/messages",
        MessagesView.as_view(),
        name="get_messages",
    ),
    path(
        "chat/<str:chat_id>/delete",
        DeleteChatView.as_view(),
        name="delete_chat",
    ),
    path(
        "chat/<str:chat_id>/leave", LeaveChatView.as_view(), name="leave_chat"
    ),
    # auth/
    path("auth/signup", UserBasicAuthView.as_view(), name="register"),
    path(
        "auth/signin", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify", TokenVerifyView.as_view(), name="token_verify"),
]
