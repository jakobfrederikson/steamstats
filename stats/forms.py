from django import forms

class SteamIDForm(forms.Form):
    steam_id = forms.CharField(label="Your Steam ID",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}
                               ))