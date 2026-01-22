from django.db import models

import datetime as dt

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
        self.lastlogoff = dt.datetime.fromtimestamp(kwargs.get("lastlogoff")) if kwargs.get("lastlogoff") is not None else None
        self.personastate = _get_persona_state(int(kwargs.get("personastate")))
        self.primaryclanid = kwargs.get("primaryclanid")
        self.timecreated = dt.datetime.fromtimestamp(kwargs.get("timecreated")) if kwargs.get("timecreated") is not None else None
        self.personastateflags = kwargs.get("personastateflags")
        
        # NOT VISIBLE IF profilestate == 1
        self.loccountrycode = kwargs.get("loccountrycode") 

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, dict_obj):
        return cls(**dict_obj) 
    
def _get_persona_state(state):
    if state == 0:
        return "0 - Offline"
    elif state == 1:
        return "1 - Online"
    elif state == 2:
        return "2 - Busy"
    elif state == 3:
        return "3 - Away"
    elif state == 4:
        return "4 - Snooze"
    elif state == 5:
        return "5 - Looking to trade"
    elif state == 6:
        return "6 - Looking to play"


class GameInformation(models.Model):
    name = models.CharField()
    img_icon_url = models.URLField()
    appid = models.IntegerField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField()
    final_formatted = models.CharField()
    last_updated = models.DateTimeField()


class OwnedGamesDTO():
    game_information: GameInformation

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
        self.rtime_last_played = dt.datetime.fromtimestamp(kwargs.get("rtime_last_played")) if kwargs.get("rtime_last_played") is not None else None
        self.content_descriptorids = kwargs.get("content_descriptorids")
        self.playtime_disconnected = kwargs.get("playtime_disconnected")

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, dict_obj):
        return cls(**dict_obj)
    
    @property
    def price_per_hour(self):
        if not self.game_information or self.playtime_forever <= 0:
            return 0
        if self.game_information.final_formatted == "FREE":
            return 0
        return round(float(self.game_information.price) / self.playtime_forever, 2)
    
    @property
    def icon_url(self):
        if self.game_information and self.game_information.img_icon_url:
            return self.game_information.img_icon_url
        return f"https://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.img_icon_url}.jpg"