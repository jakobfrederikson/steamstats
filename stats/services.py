import requests
from django.conf import settings

def get_steam_player_summary(steam_id):
    """
    Business logic for fetching steam data about  
    
    :param steam_id: The user's steam ID as a number
    """
    params = {
        'key': settings.STEAM_API_KEY,
        'steamids': steam_id
    }

    res = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params)
    return res
