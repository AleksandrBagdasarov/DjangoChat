from api.actions.auth import UserBasicAuthView
from api.actions.chat import (
    ChatByNameView,
    DeleteChatView,
    LeaveChatView,
    MessagesView,
    NewChatView,
)
from api.actions.dashboard import ChatToMessageByDateView, UserToMessageView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # dashboard/
    path(
        "dashboard/one-chat",
        UserToMessageView.as_view(),
        name="dashboard-user_to_message",
    ),
    path(
        "dashboard/all-chats",
        ChatToMessageByDateView.as_view(),
        name="dashboard-chat_to_message",
    ),
    # chat/
    path("chat", NewChatView.as_view(), name="new_chat"),
    path("chat/search", ChatByNameView.as_view(), name="search-chat_by_name"),
    path(
        "chat/messages",
        MessagesView.as_view(),
        name="get_messages",
    ),
    path(
        "chat/delete",
        DeleteChatView.as_view(),
        name="delete_chat",
    ),
    path("chat/leave", LeaveChatView.as_view(), name="leave_chat"),
    # auth/
    path("auth/signup", UserBasicAuthView.as_view(), name="register"),
    path(
        "auth/signin", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify", TokenVerifyView.as_view(), name="token_verify"),
]
