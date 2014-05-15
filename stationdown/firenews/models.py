# stationdown/firenews/models.py
import re
import os
import feedparser
import csv
import warnings
import requests
import time
import unicodecsv
from django.contrib.gis.db import models
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
import stationdown.firenews.models
from stationdown.firenews.models import *
import stationdown.firenews.geocoder
from stationdown.firenews.geocoder import *
from stationdown.firenews.fire_incident import *

class FireNewsFeed:

	# for debugging, set to True and the class will retreive only the first
	# page and try to store those entries
	def save(self):
		incidents = self.fetchPages()

		for incident in incidents:
			g = Geocoder()
			point = g.geocode( incident.fireAddress )
			incident.point = GEOSGeometry( 'POINT({0} {1})'.format(point.longitude, point.latitude) )
			print "saving incident from {0} at {1} with lat:{2} lng:{3}".format( incident.fireDate, incident.fireAddress, incident.point.coords[0], incident.point.coords[1] ) 
			incident.save()
				
	# given the page number return the url that we would use to
	# retreive it
	def url( self, page ):
	
		# we've disabled follow redirects so if you pass page = 1, 
		# it will try to redirect to general feed/
		# so if page = 1, we need to give it the general feed url
		if page == 1:
			return "http://www.phillyfirenews.com/category/fire_wire/pennsylvania/city-of-philadelphia/feed/"
		else:
			return "http://www.phillyfirenews.com/category/fire_wire/pennsylvania/city-of-philadelphia/feed/?paged=" + str(page)

	# head to the site and return the xml feed pages as strings
	def fetchPages(self):

		count = 1
		fireIncidentsList = []
		done = False
		while not done:
			print "retreiving prage " + str(count) + " from Philly Fire News feed"

			url = self.url( count ) 
			response = requests.get(url, allow_redirects=False)
			responseCode = response.status_code
			xmlStr = response.text

			if responseCode == 200:
				# add on the list returned to fireIncidentsList
				fireIncidentsList.extend( self.parseXmlPage(xmlStr) )
				count += 1
			else:
				done = True

			#set second boolean to false if you just want to check a 1 page download
			if count > 1 and self.justOnePage:
				done = True

		return fireIncidentsList
		
	# given an xml string, parse it into items and fill up incident
	# objects
	def parseXmlPage( self, xmlStr ):
		d = feedparser.parse( xmlStr )

		fireIncidents = []
		incidentManager = FireIncidentManager()
		for entry in d.entries:
			fireIncidents.append( incidentManager.create_feed_entry( entry ) )
			
		if len(fireIncidents) == 0:
			warnings.warn( "was unable to create any fire incidents from xml page" )
			
		return fireIncidents
	
