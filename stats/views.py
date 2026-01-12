from django.http import HttpResponse
from django.shortcuts import render

from stats import services

# Create your views here.
def index(request):
    steamid = 76561197999242706
    return HttpResponse(services.get_steam_player_summary(steamid))