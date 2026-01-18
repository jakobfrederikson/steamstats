import requests
from django.conf import settings
from .models import PlayerSummaryDTO, OwnedGamesDTO

steam_api_key = settings.STEAM_API_KEY
format = "json"

# TODO:
# 1. add support for https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=steam_api_key&vanityurl={UsersCustomURL}
# 2. response looks as so: {"response":{"steamid":"76561198087999365","success":1}}
def get_steam_player_summary(steam_id64):
    """
    Returns a `PlayerSummaryDTO` object produced by the JSON response of ISteamUser/GetPlayerSummaries/v0002/.
    
    :param steam_id64: The 64 bit version of the user's steam id.
    """
    params = {
        'key': steam_api_key,
        'steamids': steam_id64,
        'format': format
    }

    response = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params)

    if response.status_code == requests.codes.ok:
        json_response = response.json()

        player_summary_dto = PlayerSummaryDTO.from_dict(json_response['response']['players'][0])

        return player_summary_dto
    else:
        return response.status_code
    
def get_steam_player_level(steam_id64):
    """
    Returns a an `int player_level` produced by the JSON response of IPlayerService/GetSteamLevel/v1/.
    
    :param steam_id64: The 64 bit version of the user's steam id.
    """
    params = {
        'key': steam_api_key,
        'steamid': steam_id64,
        'format': format
    }

    response = requests.get('http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/', params)

    if response.status_code == requests.codes.ok:
        json_response = response.json()
        player_level = int(json_response['response']['player_level'])
        return player_level
    else:
        return response.status_code
    
def get_steam_user_owned_games(steam_id64):
    """
    Returns a list of `OwnedGamesDTO` objects produced by the JSON response from the Steam API call for IPlayerService/GetOwnedGames/v0001/.
    
    :param steam_id: The 64 bit version of the user's steam id.
    """
    params = {
        'key': steam_api_key,
        'steamid': steam_id64,
        'format': format,
        'include_appinfo': 1,
        'include_played_free_games': 1,
    }

    # Response = {"response":{}} if profile is private
    response = requests.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/', params)

    if response.status_code == requests.codes.ok:
        json_response = response.json()

        # If user's profile is private, return empty
        if json_response == {"response": {}}:
            return {}

        owned_games_dtos = []
        
        for game in json_response['response']['games']:
            owned_games_dtos.append(OwnedGamesDTO.from_dict(game))

        owned_games_dtos.sort(reverse=True, key=sort_by_playtime)

        return owned_games_dtos
    else:
        return response.status_code


def sort_by_playtime(e: OwnedGamesDTO):
    return e.playtime_forever

# TODO:
# 1. Get game price via country code??
# 2. https://store.steampowered.com/api/appdetails?filters=price_overview&appids=620




