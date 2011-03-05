from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^kexp/', include('kexp.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^$', 'sKrEXP-server.tag.views.index'),
#    (r'^artist/(?P<artist>[^/]*)/?$', 'tag.views.artist'),
#    (r'^song/(?P<song>[^/]*)/?$', 'tag.views.song'),
    (r'^time_to_song/year=(?P<year>[^/]*)&month=(?P<month>[^/]*)&day=(?P<day>[^/]*)&hour=(?P<month>[^/]*)/?$', 'tag.views.time_to_song'),
    (r'^times_to_songs/?$', 'tag.views.times_to_songs'),
	(r'^day=(?P<day>[^/]*)/?$', 'tag.views.day'),
    (r'^recent/?$', 'tag.views.recent'),
    (r'^admin/', include(admin.site.urls)),
)
