import requests
from django.conf import settings

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
    Returns the json object result of GetOwnedGames from the steam API if the user's steam ID is valid.
    
    :param steam_id: the users steam ID
    """
    params = {
        'key': steam_api_key,
        'steamid': steam_id,
        'format': format
    }

    response = requests.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/', params)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return response.status_code
