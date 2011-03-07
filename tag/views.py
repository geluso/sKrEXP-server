from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from tag.models import Song, RadioPlay, UserFavorites
from tag import skrexper
from django.core import serializers

from datetime import datetime
import simplejson, urllib2, urllib
from tag.BeautifulSoup import BeautifulSoup as Soup

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

def day(request, day):
	response = HttpResponse()
	json_serializer = serializers.get_serializer("json")()

	query = RadioPlay.objects.filter(time__day=day)
	json_serializer.serialize(query, ensure_ascii=False, stream=response)

	return response

def hour(request, date):
	return HttpResponse(date)

def recent(request):
	skrexper.SLOW = True
	skrexper.scrape_hour()
        skrexper.SLOW = False
	query = RadioPlay.objects.order_by("-time")[:10]
        result = [play.gather_fields() for play in query]
        return HttpResponse(simplejson.dumps(result))

# given a list of song ids, this returns a list of songs.
def times_to_songs(request, times):
    times = times.split(",")
    songs = []
    for target_time in times:
	song = RadioPlay.objects.order_by('-time').filter(time__lte=target_time)
	if song:
	    song22 = song[0].song
            fav = UserFavorites(song=song22)
            fav.save()
            songs.append(song22)
    if len(songs) <= 0:
	return HttpResponse(simplejson.dumps([{"album": "not found", "song_id": 1, "title": "not found", "artist": "not found", "song_year": "", "label": ""}]))
    songs = [song.gather_fields() for song in songs]
    return HttpResponse(simplejson.dumps(songs))

# given a list of song ids, this returns a list of songs.
def ids_to_songs(request, ids):
    response = HttpResponse()
    json_serializer = serializers.get_serializer("json")()
    
    ids = ids.split(",")
    
    query = Song.objects.filter(pk__in=ids)
    json_serializer.serialize(query, ensure_ascii=False, stream=response)
    return response

def now(request):
    favorites = [song.id for song in RadioPlay.objects.order_by("-time")[:10]]
    tinies = ""
    for favorite in favorites:
        favorite = Song.objects.get(pk=favorite) 
        tiny = get_tiny(favorite.title + " " + favorite.artist)
	if tiny is not None:
	    tinies += str(tiny) + ","
    return HttpResponse(tinies[:-1])

def one(request):
    skrexper.scrape_hour()
    song = RadioPlay.objects.all().order_by("-time")[0]
    return HttpResponse(unicode(song))

def favorites(request):
    favorites = UserFavorites.objects.all()
    tinies = ""
    for favorite in favorites:
        tiny = get_tiny(favorite.song.title + " " + favorite.song.artist)
	if tiny is not None:
	    tinies += str(tiny) + ","
    return HttpResponse(tinies[:-1])

def get_tiny(song):
    song = urllib.pathname2url(song)
    url = "http://tinysong.com/b/%s?format=json&key=81fa14156b39c1e4798f6155a1e01a10" % song
    result = urllib2.urlopen(url).read()
    if result:
        result = result[result.find("SongID") + 8:]
	result = result[:result.find(",")]
	if not result.find("missing") >= 0:
		return result
    return None
