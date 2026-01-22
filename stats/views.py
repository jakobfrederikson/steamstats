from django.shortcuts import render, redirect

from stats import services
from .forms import SteamIDForm
from .models import OwnedGamesDTO

from stats.SteamIDConverterPython.SteamID import SteamID, InvalidSteamID

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SteamIDForm(request.POST)
        if form.is_valid():
            steam_id = form.cleaned_data['steam_id']
            return redirect('detail', steam_id=steam_id)
    else:
        form = SteamIDForm()
        context = {
            'form': form
        }

    return render(request, 'index.html', context=context)    


# Display details about a user after receiving their steam ID
def detail(request, steam_id):
    try:
        steam_id_obj = SteamID(steam_id)
        steam_ids = {
            'steamid': steam_id_obj.get_steam_id(),
            'steamid3': steam_id_obj.get_steam_id3(),
            'steam32id': steam_id_obj.get_steam32_id(),
            'steam64id': steam_id_obj.get_steam64_id()
        }

        player_summary = services.get_steam_player_summary(steam_ids['steam64id'])
        player_level = services.get_steam_player_level(steam_ids['steam64id'])
        steam_data_owned_games = services.get_steam_user_owned_games(steam_ids['steam64id'])

        playtimes = [game.playtime_forever == 0 for game in steam_data_owned_games]
        if all(playtimes):
            possible_playtime_set_private = True
            owned_games_with_game_information = steam_data_owned_games
            owned_games_with_game_information.sort(key=sort_by_name)
        else:
            possible_playtime_set_private = False
            owned_games_with_game_information = services.get_game_information_from_db(steam_data_owned_games)

        context = {
            'player_summary': player_summary,
            'player_level': player_level,
            'steam_ids': steam_ids,
            'games': owned_games_with_game_information,
            'possible_playtime_set_private': possible_playtime_set_private,
        }
        
        return render(request, 'stats/detail.html', context=context)
    except InvalidSteamID:
        # send back to index advising Steam ID not valid
        pass
    return render(request, "index.html", context=context)


# ==================
#     Helper(s)
# ==================
def sort_by_name(e: OwnedGamesDTO):
    return e.name