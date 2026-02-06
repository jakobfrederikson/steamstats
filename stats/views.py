from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone

from stats import services
from .forms import SteamIDForm
from .models import OwnedGamesDTO, GameInformation, UniqueGameHit

from stats.SteamIDConverterPython.SteamID import SteamID, InvalidSteamID

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SteamIDForm(request.POST)
        if form.is_valid():
            steam_id = form.cleaned_data['steam_id']
            return redirect('detail', steam_id=steam_id)
    else:
        form = SteamIDForm()
        context = {}
        context["form"] = form

    return render(request, 'index.html', context=context)


# Display details about a user after receiving their steam ID
def detail(request, steam_id):
    steam_ids = {}
    # Try succesfully convert steam ID
    try:
        steam_id_obj = SteamID(steam_id)
        steam_ids['steamid'] = steam_id_obj.get_steam_id()
        steam_ids['steamid3'] = steam_id_obj.get_steam_id3()
        steam_ids['steam32id'] = steam_id_obj.get_steam32_id()
        steam_ids['steam64id'] = steam_id_obj.get_steam64_id()
    # Maybe user input their custom steam URL instead of their SteamID, so try and get that.
    except InvalidSteamID:
        try:
            steam_id_from_custom_url = services.try_get_steam_id_from_custom_url(steam_id)
            steam_id_obj = SteamID(steam_id_from_custom_url)
            steam_ids['steamid'] = steam_id_obj.get_steam_id()
            steam_ids['steamid3'] = steam_id_obj.get_steam_id3()
            steam_ids['steam32id'] = steam_id_obj.get_steam32_id()
            steam_ids['steam64id'] = steam_id_obj.get_steam64_id()
        # If we still can't get a valid SteamID, then user probably input something that is not a SteamID
        except InvalidSteamID:
            return redirect('index')
        
    player_summary = services.get_steam_player_summary(steam_ids['steam64id'])
    player_level = services.get_steam_player_level(steam_ids['steam64id'])
    steam_data_owned_games = services.get_steam_user_owned_games(steam_ids['steam64id'])

    owned_games_with_game_information = services.get_game_information_from_db(steam_data_owned_games)

    for game in owned_games_with_game_information:
        obj, created = UniqueGameHit.objects.get_or_create(
            game = game.game_information,
            steam64id=steam_ids['steam64id']
        )

        # if a new unique game hit was created, then update 'last_updated' to now in game_information table
        if created:
            game_info_obj = obj.game
            game_info_obj.last_updated = timezone.now()
            game_info_obj.save(update_fields=["last_updated"])

    playtimes_equal_zero = [game.playtime_forever == 0 for game in owned_games_with_game_information]
    if all(playtimes_equal_zero):
        possible_playtime_set_private = True
        owned_games_with_game_information.sort(key=sort_by_price, reverse=True)
    else:
        possible_playtime_set_private = False

    total_hours_played = 0
    total_dollars_spent = 0
    for game in owned_games_with_game_information:
        total_hours_played += game.playtime_forever
        total_dollars_spent += float(game.game_information.price)
    
    total_dollars_spent = round(total_dollars_spent, 2)
    total_hours_played = round(total_hours_played, 2)

    context = {
        'player_summary': player_summary,
        'player_level': player_level,
        'steam_ids': steam_ids,
        'total_hours_played': total_hours_played,
        'total_dollars_spent': total_dollars_spent,
        'games': owned_games_with_game_information,
        'possible_playtime_set_private': possible_playtime_set_private,
    }
    
    return render(request, 'stats/detail.html', context=context)


class GameInformationListView(generic.ListView):
    model = GameInformation
    context_object_name = 'games_list'
    paginate_by = 10
    template_name = 'stats/database.html'
    ordering = ['id']

    # https://docs.djangoproject.com/en/6.0/topics/class-based-views/generic-display/#dynamic-filtering
    def get_queryset(self):
        queryset = super().get_queryset()

        #QueryDict.get(key, default=None)
        # https://docs.djangoproject.com/en/6.0/ref/request-response/#django.http.QueryDict.get
        query = self.request.GET.get('q')

        column_sort = self.request.GET.get('column')

        if query:
            queryset = queryset.filter(Q(name__icontains=query))

        allowed_sort_fields = ['id', 'appid', 'name', 'price', 'last_updated']
        if column_sort in allowed_sort_fields:
            queryset = queryset.order_by(column_sort)
        else:
            queryset.order_by('id')

        return queryset
    
    # https://docs.djangoproject.com/en/6.0/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the search query
        context["search_query"] = self.request.GET.get('q', '')

        total_games = GameInformation.objects.all().count()
        context["total_games"] = total_games

        return context

def find_steam_id(request):
    return render(request, "stats/find_your_steam_id.html")


# ==================
#     Helper(s)
# ==================
def sort_by_price(e: OwnedGamesDTO):
    return e.game_information.price