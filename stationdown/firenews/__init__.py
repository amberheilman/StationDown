#from django.contrib.gis.db import models
from django.conf.urls import patterns, include, url

import os

# add firenews/templates to available html templates
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)
