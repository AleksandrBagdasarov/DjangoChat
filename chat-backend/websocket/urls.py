from api import views
from django.urls import path

urlpatterns = [
    path("<str:room_name>/", views.room_view, name="room"),
]
