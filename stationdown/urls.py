# stationdown/urls
from django.conf.urls import patterns, include, url

from stationdown.views import home
from stationdown.views import fire_stations
import stationdown.firenews

urlpatterns = patterns('',
	url(r'^$', home),
    url(r'^fire-stations/$',fire_stations),
    url(r'^fire-incidents',include(stationdown.firenews)),
)
