#from django.contrib.gis.db import models
from django.conf.urls import patterns, include, url

import os
#import xml
#from xml import *
#import tests
#from tests import *
#import re

#import stationdown.firenews.fireincidentsaver
#from fireincidentsaver import FireIncidentSaver

##import stationdown.firenews.firenewsfeed
from stationdown.firenews.firenewsfeed import FireNewsFeed

from stationdown.firenews.views import *

# add firenews/templates to available html templates
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

urlpatterns = patterns('firenews.views',
    url(r'/$',fire_home),
    url(r'/show$',show)
)