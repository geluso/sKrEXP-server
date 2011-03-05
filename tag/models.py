from django.db import models
import skrexper
import simplejson
import urllib
import time, datetime

# A song that has been played on the radio. A song should be
# uniquely identified by (artist, album, title).
# @param artist, album, song These may not be null.
# @param year, label These attributes may be null.
class Song(models.Model):
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=200, blank=True)
    label = models.CharField(max_length=200, blank=True)
    #tinysong_url = models.CharField(max_length=100, blank=True)

    def to_json(self):
        return simplejson.dumps(self.gather_fields())

    def gather_fields(self):
        fields = {}
        fields["song_id"] = self.id
        fields["artist"] = self.artist
        fields["title"] = self.title
        fields["album"] = self.album
        fields["song_year"] = self.year
        fields["label"] = self.label
        #fields["tinysong_url"] = self.tinysong_url
        return fields

    def __unicode__(self):
        return ", ".join((self.artist, self.title))

# A song played on the radio at a specific time. The time is only
# accurate to the minute. Every song played should have a unique time.
# @param time When the song was played.
# @param song The song that was played.
class RadioPlay(models.Model):
    time = models.IntegerField()
    song = models.ForeignKey(Song)
    #station = models.CharField(max_length=10)
    
    # Returns a song most 
    def get_bookmark(self, date):
        skrexper.scrape_page()
        return RadioPlay.objects.order_by('-time').filter(time__lte=str(date))[0]

    def gather_fields(self):
        date = datetime.datetime.fromtimestamp(self.time)
        fields = {}
	fields["radio_play_id"] = self.id
        fields["year"] = date.year
        fields["month"] = date.month
        fields["day"] = date.day
        fields["hour"] = date.hour
        fields["minute"] = date.minute
        fields.update(self.song.gather_fields())
        return fields

    def to_json(self):
        return simplejson.dumps(self.gather_fields())

    def __unicode__(self):
        return "\n".join((str(self.time), self.song.__unicode__()))

class UserFavorites(models.Model):
    name = models.CharField(max_length=100)
    song = models.ManyToManyField(Song)
