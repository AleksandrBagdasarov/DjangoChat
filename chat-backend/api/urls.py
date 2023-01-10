from api.actions.auth import UserBasicAuthView
from api.actions.chat import MessagesView
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path("chat/<str:chat>", MessagesView.as_view(), name="get_messages"),
    path("auth/signup", UserBasicAuthView.as_view(), name="register"),
    path(
        "auth/signin", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify", TokenVerifyView.as_view(), name="token_verify"),
]
