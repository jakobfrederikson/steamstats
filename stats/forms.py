from django import forms

class SteamIDForm(forms.Form):
    steam_id = forms.CharField(label="Your steam id")