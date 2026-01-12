from django.http import HttpResponse
from django.shortcuts import render

from stats import services

# Create your views here.
def index(request):
    steamid = 76561197999242706
    user_summary_json = services.get_steam_player_summary(steamid)

    # steam returns a list of 'players' dicts, we are only requesting one player at a time.
    steam_user_data = user_summary_json.get('response', {}).get('players', [None])[0]
    persona_name = steam_user_data['personaname']
    profile_url = steam_user_data['profileurl']

    context = { 
        'user_summary': steam_user_data,
        'persona_name': persona_name,
        'profile_url': profile_url
    }
    return render(request, 'index.html', context=context)