# stationdown/urls
from django.conf.urls import patterns, include, url

from stationdown.views import *
from stationdown.firenews.views import *
from stationdown.firestations.views import *

urlpatterns = patterns('',

	url(r'^$', home),

    url(r'^fire-stations/$', fire_stations),

    url(r'^closest-station', closest_station ),

	url(r'^fire-incidents/$', fire_home ),
	url(r'^fire-incidents/show', fire_show ),
	url(r'^fire-incidents/list', fire_list ),
	url(r'^fire-incidents/csv', fire_csv ),

    url(r'^fire-stations/get', stations_get ),
)
