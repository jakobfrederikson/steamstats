import requests
from django.conf import settings
from .models import DTO_OwnedGames

steam_api_key = settings.STEAM_API_KEY
format = "json"

def get_steam_player_summary(steam_id):
    """
    Returns the dictionary of the steam users summary.
    
    :param steam_id: The user's steam ID as a number
    """
    params = {
        'key': steam_api_key,
        'steamids': steam_id,
        'format': format
    }

    response = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params)

    if response.status_code == requests.codes.ok:
        json_response = response.json()

        # send in a workable state to the views
        # don't want too much business logic being done in views
        return json_response['response']['players'][0]
    else:
        return response.status_code
    
def get_steam_user_owned_games(steam_id):
    """
    Returns a list of games produced by the json response from the Steam API.
    
    :param steam_id: the users steam ID
    """
    params = {
        'key': steam_api_key,
        'steamid': steam_id,
        'format': format,
        'include_appinfo': 1,
        'include_played_free_games': 1,
    }

    response = requests.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/', params)
    if response.status_code == requests.codes.ok:
        json_response = response.json()
        owned_games_dtos = []
        
        for game in json_response['response']['games']:
            owned_games_dtos.append(DTO_OwnedGames.from_dict(game))
        
        for game in owned_games_dtos:
            print(f"{game.name}: {game.appid}")

        # Convert minutes to hours, 2 decimal places
        for game in json_response['response']['games']:
            game['playtime_forever'] = round(int(game['playtime_forever']) / 60, 2)
            #print(game)

        return json_response['response']['games']
    else:
        return response.status_code
