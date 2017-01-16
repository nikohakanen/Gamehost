from django.shortcuts import render
from django.http import HttpResponse
from gamehost.models import Game

# Create your views here.


# Just to test how the views worked again.
def homeview(request):

    game_list = Game.objects.all()

    return render(request, 'home.html', {'games': game_list})
