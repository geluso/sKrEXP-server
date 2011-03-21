from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from tag.models import Song, RadioPlay
from django.core import serializers

from datetime import datetime
import json

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
	response = HttpResponse()
	json_serializer = serializers.get_serializer("json")()
	
	query = RadioPlay.objects.order_by('-time')[:10]

	json_serializer.serialize(query, ensure_ascii=False, stream=response)

	return response

def time_to_songs(request, year, month, day, hour):
	date = datetime(year=year, month=month, day=day, hour=hour)
	return HttpReponse(str(date))
	
def ids_to_songs(request, ids):
	response = HTTPResponse()
	ids = ids.split(",")
	
	for idd in ids:
		
	
	return response

def times_to_songs(request):
	if request.method == "POST":
		response = HttpResponse()
		
		times = request.get("times")
		min_time = times[0]
		max_time = times[-1]
		
		RadioPlay.objects.filter(time__gte=min_time).filter(time__lte=max_time)
		json_serializer.serialize(query, ensure_ascii=False, stream=response)
		return response
	else:
		return HttpResponse("Invalid request. Must be POST.")