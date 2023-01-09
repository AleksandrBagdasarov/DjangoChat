import json

from django.shortcuts import render

# Create your views here.
# def lobby(request):
#     return render(request, "lobby.html")


def index(request):
    return render(request, "index.html", {})


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})
