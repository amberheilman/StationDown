from django.conf.urls import patterns, include, url

from stationdown.views import home
from stationdown.views import fire_stations

urlpatterns = patterns('',
	url(r'^$', home),
    url(r'^fire-stations/$',fire_stations),
)
