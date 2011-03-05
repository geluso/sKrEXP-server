from django.db import IntegrityError
import tag.BeautifulSoup as Soup

import models
import datetime
from time import mktime
import urllib2


# Url of the KEXP playlist.
PLAYLIST_URL = "http://kexp.org/playlist/playlist.aspx"
SAVE = True

# If True, displays number of songs and title, artist, album.
DEBUG = True

# If true print database errors to console
SHOW_ERRORS = True

# a useful variable used primarily when playing within the shell
NOW = datetime.datetime.now() - datetime.timedelta(hours=2)

# Returns a url for the playlist related to the given date time.
def make_url(date):
    return PLAYLIST_URL + "".join(("?t=1&year=", str(date.year), "&month=", str(date.month), "&day=", str(date.day), "&hour=", str(date.hour)))

# Loads a page representing an hour of radio time for a day. Parses each
# song on the page and registers the song in the database.
# Loads the most current hour if no URL is specified.
def scrape_page(date=None):
    if date is None:
        date = datetime.datetime.now() - datetime.timedelta(hours=2)
    url = make_url(date)
    if url is None:
        print "url is none"
    print url

    # Load the page.
    html = urllib2.urlopen(url).read()
    html = html.replace('</dt class=\"songtitle\">', "</dt>")
    page = Soup.BeautifulSoup(html)

    # Reverse list so songs played first (at bottom of playlist) are added first.
    songs = page.findAll(name="dd", attrs={"class": "song"})
    
    if(DEBUG):
        print str(len(songs)) + " songs found."
    for song in songs:
        data = Soup.BeautifulSoup(str(song))
        
        # Parse all song data.
        artist = song.findAll(name="dd", attrs={"class":"artist"})[0].contents[0]
        title = song.findAll(name="dd", attrs={"class":"songtitle"})[0].contents[0]
        time = song.findAll(name="dd", attrs={"class":"time"})[0].contents[0]
        # hack. dont worry if nothing is not found.
        try:
            album = song.findAll(name="dd", attrs={"class":"album"})[0].contents[0]
        except IndexError:
            pass
        
        if (None not in [artist, title, album, time]  and '' not in [artist, title, album, time]):
            hour = int(time[0:time.find(":")])
            minute = int(time[time.find(":") + 1:-2])
            if time[-2:] == "PM":
                hour += 12
                hour %= 24
#            if(DEBUG):
#                print title
#                print artist
#                print album
#                print
            if (SAVE):
                try:
                    new_song = models.Song(artist=artist, title=title, album=album)
                    new_song.save()

                    date = date.replace(hour=hour, minute=minute)
                    posix = int(mktime(date.timetuple()))

                    radio_play = models.RadioPlay(time=posix, song=new_song)
                    radio_play.save()
                except ValueError:
                    if (SHOW_ERRORS):
                        print "ValueError"
                        print hour, minute
                        print new_song
                        print radio_play
                        print
                except IntegrityError:
                    if (SHOW_ERRORS):
                        print "IntegrityError"
                        print new_song
                        print radio_play
                        print

# Scrapes the playlist for every song played in the last hour.
def scrape_hour():
    scrape_page()

# Scrapes the playlist for every song played today.
def scrape_today():
    now = datetime.datetime.now() - datetime.timedelta(hours=2)
    for hour in range(0, 24):
        date = datetime.datetime(now.year, now.month, now.day, hour)
        scrape_page(date)
    print len(models.Song.objects.all()), "songs,", len(models.RadioPlay.objects.all()), "radio plays"

# Scrapes the entire playlist, all the way from 2002.
def scrape_all():
    now = datetime.datetime.now() - datetime.timedelta(hours=2) - datetime.timedelta(hours=2)
    for year in range(2001, now.year + 1):
        for month in range(1, now.month + 1):
            for day in range(1, now.day + 1):
                for hour in range(0, now.hour + 1):
                    date = datetime.datetime(year, month, day, hour)
                    scrape_page(date)
            print len(Song.objects.all()), "songs,", len(RadioPlay.objects.all()), "radio plays"

# Returns the most recent song played on the radio
def most_recent():
	plays = models.RadioPlay.objects.all()
	return plays[len(plays) - 1]
	
# Scrapes the page and returns the most recently played song.
def instant():
	scrape_page(NOW)
	return most_recent()
