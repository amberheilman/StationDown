#stationdown/firenews/scrape.py
from lxml import html
import requests
import xml.etree.ElementTree as ET
from django.core.files.base import File
import os
import stationdown.settings as settings
from stationdown.firenews.models import FireNewsXmlPage, FireNewsCsv, FireNewsFeed
from stationdown.firenews.models import FeedEntry
import feedparser
from django.core.management.base import NoArgsCommand, BaseCommand, make_option

import stationdown.firenews.models
from stationdown.firenews.models import *

import stationdown.firenews.geocoder
from stationdown.firenews.geocoder import *

#
# set up a command that can be run as 'python manage.py scrape'
#
class Command(NoArgsCommand):

    help = "proper syntax: --outfile [outfile]"

    option_list = BaseCommand.option_list + (
        make_option('--verbose', action='store_true'),
        make_option('--outfile', dest='outfile',help='the output file destination for the csv'),
        make_option('--csv', action='store_true',help='the output file destination for the csv'),
        make_option('--geocode', action='store_true',help='geocode the addresses stored in the'),
        make_option('--save', action='store_true',help='save the fire news entries to the database'),
    )

    def handle(self, *args, **options):
		outfile = options['outfile']
		save = options['save']

		if 'csv' in options and options['csv'] == True:

			if outfile is None:
				raise Exception( 'outfile must be set' )

			feed = FireNewsFeed()
			pages = feed.getPages()
			csvFile = FireNewsCsv(outfile)

			for page in pages:
				entries = page.entries

				for entry in entries:
					csvFile.append( page.entries )

		elif 'save' in options and options['save'] == True:

			fireNewsEntries = FeedEntry.get()

			for page in pages:
				entries = page.entries

				for feedEntry in entries:
					feedEntry.save()

		elif 'geocode' in options and options['geocode'] == True:

			fireNewsEntries = FeedEntry.objects.all()

			for entry in fireNewsEntries:
				g = Geocoder()
				point = g.geocode( entry.fireAddress )

				if point is not None:
					print "lat: " + str(point.latitude) + " lng: " + str(point.longitude)
				else:
					print "could not geocode %s",entry.fireAddress