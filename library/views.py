from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.

def get_funFact(request):
    return render(request, 'library/funFact.html')

def get_games(request):
    return render(request, 'library/games.html')

def get_Hidetaka_Miyazaki(request):
    return render(request, 'library/Hidetaka_Miyazaki.html')


