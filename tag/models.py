from django.db import models
import skrexper

# A song that has been played on the radio. A song should be
# uniquely identified by (artist, album, title).
# @param artist, album, song These may not be null.
# @param year, label These attributes may be null.
class Song(models.Model):
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    year = models.CharField(max_length=200, blank=True)
    label = models.CharField(max_length=200, blank=True)
    station = models.CharField(max_length=6, blank=True)

    def __unicode__(self):
        return ", ".join((self.artist, self.title))

# A song played on the radio at a specific time. The time is only
# accurate to the minute. Every song played should have a unique time.
# @param time When the song was played.
# @param song The song that was played.
class RadioPlay(models.Model):
    time = models.DateTimeField('date played', unique=True)
    song = models.ForeignKey(Song)
    station = models.CharField(max_length=10)
    
    # Returns a song most 
    def get_bookmark(self, date):
        skrexper.scrape_page()
        return RadioPlay.objects.order_by('-time').filter(time__lte=str(date))[0]

    def __unicode__(self):
        return "\n".join((str(self.time), self.song.__unicode__()))
