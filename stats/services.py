import requests
from django.conf import settings

def get_steam_player_summary(steam_id):
    """
    Returns a .json() (dict) of a steam users summary
    
    :param steam_id: The user's steam ID as a number
    """
    params = {
        'key': settings.STEAM_API_KEY,
        'steamids': steam_id
    }

    response = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params)

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return response.status_code
