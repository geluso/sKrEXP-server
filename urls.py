from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^$', 'sKrEXP-server.tag.views.index'),
    (r'^ids_to_songs/(?P<ids>[^/]*)/?$', 'tag.views.ids_to_songs'),
    (r'^times_to_songs/(?P<times>[^/]*)/?$', 'tag.views.times_to_songs'),
    (r'^add_to_favorites/(?P<song_id>[^/]*)/?$', 'tag.views.add_to_favorites'),
    (r'^remove_from_favorites/(?P<favorite_id>[^/]*)/?$', 'tag.views.remove_from_favorites'),
    (r'^day=(?P<day>[^/]*)/?$', 'tag.views.day'),
    (r'^recent/?$', 'tag.views.recent'),
    (r'^play_recent/?$', 'tag.views.play_recent'),
    (r'^play_favorites/?$', 'tag.views.play_favorites'),
    (r'^favorites/?$', 'tag.views.favorites'),
    (r'^now/?$', 'tag.views.now'),
    (r'^one/?$', 'tag.views.one'),
    (r'^admin/', include(admin.site.urls)),
)
