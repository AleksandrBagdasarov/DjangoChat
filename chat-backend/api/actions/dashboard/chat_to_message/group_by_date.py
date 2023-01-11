from api.actions.dashboard.chat_to_message.serializer import (
    ChatToMessageByDateSerializer,
)
from django.db import connection
from rest_framework import generics, permissions


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def query():
    sql = """
    with two_weeks as (
        select date_trunc('day', one_day) as one_day
        from generate_series(
            (
                now() - interval '14 days'),
                now(),
                '1 day'
            ) one_day
        )
    select
        c.name as chat_name,
        c.id as chat_id,
        date(tw.one_day) as day,
        count(m.user_id) as message_quantity
    from two_weeks tw
    left join message m on (date(tw.one_day) = date(m.created_at))
    left join chat c on c.id = m.chat_id
    group by c.name, c.id, tw.one_day
    order by tw.one_day;

    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = dictfetchall(cursor)
    return result


class ChatToMessageByDateView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    serializer_class = ChatToMessageByDateSerializer

    def get_queryset(self):
        queryset = query()
        return queryset
