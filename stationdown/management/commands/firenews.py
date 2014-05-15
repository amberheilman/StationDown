#stationdown/firenews/scrape.py
from lxml import html
import requests
import xml.etree.ElementTree as ET
from django.core.files.base import File
import os

import feedparser
from django.core.management.base import NoArgsCommand, BaseCommand, make_option
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point as GEOSPoint

import stationdown.settings as settings
from stationdown.firenews.models import *
from stationdown.firenews.models import *
import stationdown.firenews.geocoder
from stationdown.firenews.geocoder import *

#
# set up a command that can be run as 'python manage.py scrape'
#
class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--save', action='store_true',help='save the fire news entries to the database'),
    )

    def handle(self, *args, **options):
		save = options['save']

		if 'save' in options and options['save'] == True:

			feed = FireNewsFeed()
			feed.save()
