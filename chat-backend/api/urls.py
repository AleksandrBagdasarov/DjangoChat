from api.actions.dashboard import ChatToMessageByDateView, UserToMessageView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from api.views.auth import UserBasicAuthView
from api.views.chat import ChatViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('chat', ChatViewSet, basename='chat_view_set')


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
    # auth/
    path("auth/signup", UserBasicAuthView.as_view(), name="register"),
    path(
        "auth/signin", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns.extend(router.urls)
