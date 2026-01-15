from django.shortcuts import render

from stats import services
from .forms import SteamIDForm

from stats.SteamIDConverterPython.SteamID import SteamID, InvalidSteamID

# Create your views here.
def index(request):
    if request.method == "POST":
        form = SteamIDForm(request.POST)
        if form.is_valid():
            try:
                raw_steam_id = form.cleaned_data['steam_id']
                steam_id = SteamID(raw_steam_id)
                steam_id64 = steam_id.get_steam64_id()

                player_summary = services.get_steam_player_summary(steam_id64)
                owned_games = services.get_steam_user_owned_games(steam_id64)

                persona_name = player_summary['personaname']
                profile_url = player_summary['profileurl']
                
                context = {
                    'show_steam_stats': 'yes',
                    'form': form,
                    'user_summary': player_summary,
                    'owned_games': owned_games,
                    'persona_name': persona_name,
                    'profile_url': profile_url
                }
                # re-render the page with new context
                return render(request, 'index.html', context=context)
            except InvalidSteamID:
                form.add_error('steam_id', "The steam ID provided is invalid.")
    else:
        form = SteamIDForm()

    context = {
        'form': form,
        'show_steam_stats': 'no'
    }    
    
    return render(request, 'index.html', context=context)    
