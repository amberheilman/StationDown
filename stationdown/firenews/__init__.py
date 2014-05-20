from django.contrib.gis.db import models

import os
import xml
from xml import *
import tests
from tests import *
import re

import stationdown.firenews.fireincidentsaver
from fireincidentsaver import FireIncidentSaver

import stationdown.firenews.firenewsfeed
from stationdown.firenews.firenewsfeed import FireNewsFeed

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

