from django.http import HttpResponse
from django.shortcuts import render
from .forms import PlayerForm
from django.forms import formset_factory
from home.models import ActivePlayer, Player

def index(request):
    return render(request, 'home/index.html')
    
def player_entry(request):

    context = {}

    RedPlayerFormSet = formset_factory(PlayerForm, extra=19)
    BluePlayerFormSet = formset_factory(PlayerForm, extra=19)
    #manage_data with these params is required for each
    manage_data_red = { 'red-TOTAL_FORMS': '15', 'red-INITIAL_FORMS': '0',}
    manage_data_blue = { 'blue-TOTAL_FORMS': '15', 'blue-INITIAL_FORMS': '0',}
    red_player_formset = RedPlayerFormSet(manage_data_red, prefix="red")
    blue_player_formset = BluePlayerFormSet(manage_data_blue, prefix="blue")

    players_saved = False

    if request.method == 'POST':
        post = request.POST
        # separate the red form data from the blue form data
        post_data_red = {}
        post_data_blue = {}
        active_data = {}
        for key in post:
            if "red-" in key:
                post_data_red[key] = post[key]
                # assigns player id to red
                if "-id" in key and post[key] != "" and post[key] not in active_data:
                    active_data[post[key]] = "RED"
            elif "blue-" in key:
                post_data_blue[key] = post[key]
                # assigns player id to blue
                if "-id" in key and post[key] != "" and post[key] not in active_data:
                    active_data[post[key]] = "BLUE"
        # make a formset for the 2 forms. must pass them the right prefix so that it knows to take it off for the save()
        red_player_formset = RedPlayerFormSet(post_data_red, prefix="red")
        blue_player_formset = BluePlayerFormSet(post_data_blue, prefix="blue")
        # must validate data otherwise it won't clean it and create the cleaned_data member for save()
        red_player_formset.is_valid()
        blue_player_formset.is_valid()
        # for both formsets need to loop through each form to save individual forms
        for form in red_player_formset:
            if form.is_valid() and form.cleaned_data: #form must be valid and non-empty before saving
                form.save()
        for form in blue_player_formset:
            if form.is_valid() and form.cleaned_data: #form must be valid and non-empty before saving
                form.save()
        # adds posted players to active player table
        ActivePlayer.objects.all().delete()
        for id in active_data:
            if active_data[id] == "RED":
                player = Player.objects.get(pk = id)
                ActivePlayer.objects.create(player_info = player,team = "RED")
            else:
                player = Player.objects.get(pk = id)
                ActivePlayer.objects.create(player_info = player,team = "BLUE")
        players_saved = True

    context = {
        'title': 'Player Entry',
        'red_player_formset': red_player_formset,
        'blue_player_formset': blue_player_formset,
        'players_saved': players_saved
    }

    return render(request, 'home/player_entry.html', context)
    
def game_action(request):
    # make a list of all the players for each team
    context = {
        'title': 'Game Action',
        'red_team': ActivePlayer.objects.filter(team="RED"),
        'blue_team': ActivePlayer.objects.filter(team="BLUE"),
    }
    
    return render(request, 'home/game_action.html', context)