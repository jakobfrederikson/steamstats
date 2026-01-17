from django.shortcuts import render

from stats import services
from .forms import SteamIDForm

from stats.SteamIDConverterPython.SteamID import SteamID, InvalidSteamID

# Create your views here.
def index(request):
    form = SteamIDForm()

    context = {
        'form': form
    }    
    
    return render(request, 'index.html', context=context)    


def stats_detail(request):
    if request.method == 'POST':
        form = SteamIDForm(request.POST)
        if form.is_valid():
            try:
                raw_steam_id = form.cleaned_data['steam_id']
                steam_id_obj = SteamID(raw_steam_id)

                steam_ids = {
                    'steamid': steam_id_obj.get_steam_id(),
                    'steamid3': steam_id_obj.get_steam_id3(),
                    'steam32id': steam_id_obj.get_steam32_id(),
                    'steam64id': steam_id_obj.get_steam64_id()
                }

                player_summary = services.get_steam_player_summary(steam_ids['steam64id'])
                owned_games = services.get_steam_user_owned_games(steam_ids['steam64id'])

                context = {
                    'show_steam_stats': 'yes',
                    'form': form,
                    'steam_ids': steam_ids,
                    'player_summary': player_summary,
                    'owned_games': owned_games,
                }
                # re-render the page with new context
                return render(request, 'stats/stats_detail.html', context=context)
            except InvalidSteamID:
                form.add_error('steam_id', "The steam ID provided is invalid.")
                context = {
                    'form' : form
                }
                return render(request, "index.html", context=context)
    else:
        index(request)