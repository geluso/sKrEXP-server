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
    (r'^day=(?P<day>[^/]*)/?$', 'tag.views.day'),
    (r'^recent/?$', 'tag.views.recent'),
    (r'^admin/', include(admin.site.urls)),
)
