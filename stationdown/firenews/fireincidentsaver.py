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
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point as GEOSPoint

import stationdown.settings as settings

from geocoder import *
from fire_incident import *
from firenewsfeed import *

class FireIncidentSaver:

	# for debugging, set to True and the class will retreive only the first
	# page and try to store those entries
	justOnePage = False

	def save(self):

		print "deleting all fire incidents in database"
		FireIncident.objects.all().delete()

		fetcher = FireNewsFeed()

		while( fetcher.hasNext() ):
			incidents = fetcher.fetchNextPage()
			self.saveIncidents( incidents, fetcher.getCurrentPageNum() )

	def saveIncidents(self,incidents, pageNum):

		count = 1
		total = len( incidents )

		for incident in incidents:
				g = Geocoder()
				point = g.geocode( incident.fireAddressStr + ", Philadelphia PA" )

				incident.x = point.longitude
				incident.y = point.latitude
				incident.point = GEOSGeometry( 
							'POINT({0} {1})'.format(point.longitude, point.latitude) )

				print "{pageNum} {count}/{total} {incident}".format(
					pageNum=pageNum,count=count, total=total,incident=incident
				 )
				
				count += 1

				if not self.incidentExists( incident ):
					incident.save()
				else:
					warnings.warn( 'incident w url ' + incident.postLinkStr + 'already exists')

	@staticmethod
	def incidentExists( incident ):
		return FireIncident.objects.filter(postLinkStr=incident.postLinkStr).count() > 0