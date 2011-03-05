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

    (r'^$', 'kexp.tag.views.index'),
    (r'^artist/(?P<artist>[^/]*)/?$', 'kexp.tag.views.artist'),
    (r'^song/(?P<song>[^/]*)/?$', 'kexp.tag.views.song'),
    (r'^hour/(?P<date>[^/]*)/?$', 'kexp.tag.views.hour'),
    (r'^admin/', include(admin.site.urls)),
)
