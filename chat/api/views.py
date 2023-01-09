import json

from django.shortcuts import render


# Create your views here.
def lobby(request):
    return render(request, "lobby.html")


def auth(request):
    return json.dumps(
        {
            "access": "",
            "refresh": "",
        }
    )
