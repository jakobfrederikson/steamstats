from django.db import models

# Create your models here.

# ===========================
# [          DTOs           ]
# ===========================

#{'response': 
# {'players': 
# [{'steamid': '76561197999242706', 
# 'communityvisibilitystate': 3, 
# 'profilestate': 1, 
# 'personaname': 'worzell', 
# 'profileurl': 'https://steamcommunity.com/profiles/76561197999242706/', 
# 'avatar': 'https://avatars.steamstatic.com/1a24480f72d5b0b199caea03a1866e1eeac489f7.jpg', 
# 'avatarmedium': 'https://avatars.steamstatic.com/1a24480f72d5b0b199caea03a1866e1eeac489f7_medium.jpg', 
# 'avatarfull': 'https://avatars.steamstatic.com/1a24480f72d5b0b199caea03a1866e1eeac489f7_full.jpg', 
# 'avatarhash': '1a24480f72d5b0b199caea03a1866e1eeac489f7', 
# 'lastlogoff': 1768464262, 
# 'personastate': 0, 
# 'primaryclanid': '103582791456245411', 
# 'timecreated': 1213262345, 
# 'personastateflags': 0, 
# 'loccountrycode': 'NZ'}]}}

class PlayerSummaryDTO():
    def __init__(self, **kwargs):
        self.steamid = kwargs.get("steamid")
        self.communityvisibilitystate = kwargs.get("communityvisibilitystate")
        self.profilestate = kwargs.get("profilestate")
        self.personaname = kwargs.get("personaname")
        self.profileurl = kwargs.get("profileurl")
        self.avatar = kwargs.get("avatar")
        self.avatarmedium = kwargs.get("avatarmedium")
        self.avatarfull = kwargs.get("avatarfull")
        self.avatarhash = kwargs.get("avatarhash")
        self.lastlogoff = kwargs.get("lastlogoff")
        self.personastate = kwargs.get("personastate")
        self.primaryclanid = kwargs.get("primaryclanid")
        self.timecreated = kwargs.get("timecreated")
        self.personastateflags = kwargs.get("personastateflags")
        self.loccountrycode = kwargs.get("loccountrycode")      

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, dict_obj):
        return cls(**dict_obj) 
    

# {'appid': 3240220, 
# 'name': 'Grand Theft Auto V Enhanced', 
# 'playtime_forever': 0.0, 
# 'img_icon_url': '8355a7bbdb704f727bfba80ec56bc7228991338e', 
# 'has_community_visible_stats': True, 
# 'playtime_windows_forever': 0, 
# 'playtime_mac_forever': 0, 
# 'playtime_linux_forever': 0, 
# 'playtime_deck_forever': 0, 
# 'rtime_last_played': 0, 
# 'content_descriptorids': [1, 2, 5], 
# 'playtime_disconnected': 0}
# https://hackernoon.com/dto-in-python-an-explanation
class OwnedGamesDTO():
    def __init__(self, **kwargs):
        self.appid = kwargs.get("appid")
        self.name = kwargs.get("name")
        self.playtime_forever = round(kwargs.get("playtime_forever") / 60, 2)
        self.img_icon_url = kwargs.get("img_icon_url")
        self.has_community_visible_stats = kwargs.get("has_community_visible_stats")
        self.playtime_windows_forever = kwargs.get("playtime_windows_forever")
        self.playtime_mac_forever = kwargs.get("playtime_mac_forever")
        self.playtime_linux_forever = kwargs.get("playtime_linux_forever") 
        self.playtime_deck_forever = kwargs.get("playtime_deck_forever")
        self.rtime_last_played = kwargs.get("rtime_last_played")
        self.content_descriptorids = kwargs.get("content_descriptorids")
        self.playtime_disconnected = kwargs.get("playtime_disconnected")

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, dict_obj):
        return cls(**dict_obj)