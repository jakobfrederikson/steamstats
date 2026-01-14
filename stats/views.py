from django.http import HttpResponse
from django.shortcuts import render

from stats import services

# Create your views here.
def index(request):
    steamid = 76561197999242706
    player_summary = services.get_steam_player_summary(steamid)
    owned_games = services.get_steam_user_owned_games(steamid)

    persona_name = player_summary['personaname']
    profile_url = player_summary['profileurl']
    
    context = {
        'user_summary': player_summary,
        'owned_games': owned_games,
        'persona_name': persona_name,
        'profile_url': profile_url
    }
    return render(request, 'index.html', context=context)
