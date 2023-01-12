from urllib.parse import parse_qs

from api.models import User
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class QueryAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        dict_query = parse_qs(scope["query_string"].decode())
        access = dict_query.get("access")
        refresh = dict_query.get("refresh")

        if access:
            payload = AccessToken(token=access[0])
        elif refresh:
            refresh = RefreshToken(token=refresh[0])
            payload = refresh.access_token
        else:
            payload = {}

        scope["user"] = await get_user(payload.get("user_id", -1))
        return await self.app(scope, receive, send)
