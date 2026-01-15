from django.db import models

# Create your models here.

# ===========================
# [          DTOs           ]
# ===========================

class PlayerSummaryDTO():
    pass

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
        self.playtime_forever = kwargs.get("playtime_forever")
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