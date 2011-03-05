from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from kexp.tag.models import Song, RadioPlay

def index(request):
    recently_played = RadioPlay.objects.order_by('-time')[:50]
    return render_to_response('skrexp/home.html', \
        {'recently_played' : recently_played})

def artist(request, artist):
    artist_songs = Song.objects.filter(artist=artist)
    template = loader.get_template("skrexp/artist.html")
    context = Context({
        'artist_songs' : artist_songs
    })
    return HttpResponse(template.render(context))

def song(request, song):
    return HttpResponse(song)

def hour(request, date):
    return HttpResponse(date)
