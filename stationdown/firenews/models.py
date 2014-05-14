# stationdown/firenews/models.py
from django.db import models
import re
import os
import feedparser
import csv
import warnings
import requests
import time
import unicodecsv
#from django.contrib.gis.db import models

#
# FeedEntry is a container for the information stored in each Philly Fire News post
#
class FeedEntry(models.Model):

	id = models.AutoField(primary_key=True)

	postTitle = models.CharField(max_length=255)
	postLink  = models.CharField(max_length=255)
	postDate  = models.CharField(max_length=255)
	
	fireDate = models.CharField(max_length=255)
	fireTime = models.CharField(max_length=255)
	fireAddress = models.TextField()
	fireType = models.CharField(max_length=255)
	fireDetails = models.TextField()

	#point = models.PointField()

class FeedEntryManager(models.Manager):

	def create_feed_entry( self, dataList ):
		feedEntry = FeedEntry()
		feedEntry.postTitle = dataList.title
		feedEntry.postLink  = dataList.link
		feedEntry.postDate  = dataList.published 
		
		contentHtml = PostContentHtml( dataList.content )
		feedEntry.fireDate = dataList.fireDate
		feedEntry.fireTime = dataList.fireTime
		feedEntry.fireAddress = dataList.fireAddress
		feedEntry.fireType = dataList.fireType
		feedEntry.fireDetails = dataList.fireDetails

		return feedEntry

class FireNewsFeed:

	def __init__(self):
		pass

	def url( self, page ):
	
		# we've disabled follow redirects so if you pass page = 1, 
		# it will try to redirect to general feed/
		# so if page = 1, we need to give it the general feed url
		if page == 1:
			return "http://www.phillyfirenews.com/category/fire_wire/pennsylvania/city-of-philadelphia/feed/"
		else:
			return "http://www.phillyfirenews.com/category/fire_wire/pennsylvania/city-of-philadelphia/feed/?paged=" + str(page)

	def getPages(self):

		count = 1
		xmlPages = []
		done = False
		while not done:
			print "retreiving page " + str(count) + " from Philly Fire News feed"

			url = self.url( count ) 
			response = requests.get(url, allow_redirects=False)
			responseCode = response.status_code
			xmlStr = response.text

			if responseCode == 200:
				xmlPages.append( FireNewsXmlPage(xmlStr) )
				count += 1
			else:
				done = True

			#uncomment if you just want to check a 1 page download
			if count > 1 and False:
				done = True

		return xmlPages

#
# we need a container for the xml string that contains fire data
#
class FireNewsXmlPage:
	def __init__(self, source):
		self.source = source
		self.parse()

		if len(self.entries) == 0:
			warnings.warn("no fire entries in xml page")

	def parse(self):

		self.entries = []

		#if os.path.isfile(self.source): # if source is a file
		d = feedparser.parse( self.source )

		for entry in d.entries:
			self.entries.append( FeedEntry( entry ) )

	def entries(self):
		return self.entries
	
#
# PostContentHtml is the container and parser for the fire details contained in the wordpress post html
#
class PostContentHtml:
	
	# feedparser fills entry.content with a list, be prepared for it
	def __init__( self, contentList ):

		# feedparser puts content into a list because atom feeds may have multiples, we need a string
		contentStr = ' '.join(contentList)
		#contentStr = self.listToString( contentList )

		self.fireDate = self.getFireDate( contentStr )
		self.fireTime = self.getFireTime( contentStr )
		self.fireAddress = self.getFireAddress( contentStr )
		self.fireType = self.getFireType( contentStr )
		self.fireDetails = self.getFireDetails( contentStr )


	def listToString( self, contentList ):
		retVal = ""
		for c in contentList:
			retVal += c.value
		
		return retVal

	# fire info in posts is labeled a few ways, matchByRegexList takes a list of regexes
	# and returns the match from the first regex tested against contentStr
	def matchByRegexList( self, searchDescription, regexList, contentStr ):

		for regex in regexList:

			m = re.search( regex, contentStr, flags=re.IGNORECASE );

			if( m is not None ): # found it!, let's send it back
				return m.group(1).strip()

		# if all goes well, we should already have returned
		warnings.warn( "unable to find " + searchDescription 
						+ " with regex " + ", ".join(regexList) + " and content:\n\n==>" 
						+ contentStr.encode('utf-8','replace') + '<==')
		return None	

	# get the date of fire from the post content string
 	def getFireDate(self, contentStr):
 		regexList = [
 			'<strong>Date:*\s*</strong>(.+)<br />', 
 			'<p>Date:\s*(.+)<',
 			'Date:\s*(.+)<',
 			'<p>(09/06/13)</p>' # page 21 has a a real tough one
 		]
 		return self.matchByRegexList('FireDate', regexList, contentStr )

	# get the time of the fire from the post content string
	def getFireTime(self, contentStr):
		regexList = [ 
			'<strong>Time:*\s*</strong>(.+)<br />', 
			'>Time:\s*(.+)<',
			'Time:\s*(.+)<',
			'<p>(10:10)</p>' # a hard coded date
		]
		return self.matchByRegexList('FireTime',regexList,contentStr)

	# get the time of the fire from the post content string
	def getFireAddress(self, contentStr):
		regexList = [ 
			'<strong>Address:*\s*</strong>(.+)<br />',
			'<strong>Address:*\s*</strong>(.+)</p>',
			'<p>Address:\s*(.+)</p>',
			'Address:\s*(.+)<br',
			'<p>(Cambria and Rosehill)</p>' # a hard coded address
		]
		return self.matchByRegexList('FireAddress',regexList,contentStr)

	# get the time of the fire from the post content string
	def getFireType(self, contentStr):
		regexList = [ 
			'<strong>Type:*\s*</strong>(.+)<br\s*/>', 
			'<strong>Type:*\s*</strong>(.+)</p>', 
			'<p>Type:\s*(.+)</p>',
			'Type:\s*(.+)<br />',
			'()' # there are posts with no type 
		]
		return self.matchByRegexList('FireType',regexList,contentStr)

	# get the time of the fire from the post content string
	def getFireDetails(self, contentStr):

		m = re.search( '<p>(.+)</p>$', contentStr );

		regexList = [ 
			'<strong>Details:\s*</strong>(.+)', 
			'<p>Details:\s*(.+)</p>',
			'\nDetails:\s*(.+)</p>$',
			'<p>(.+)</p>$'
		 ]
 		return self.matchByRegexList('FireDetails', regexList, contentStr)

class FireNewsCsv:

	def __init__(self, outfile):

		# if outfile is empty, raise exception
		if( outfile is None ):
			raise ValueError('outfile may not be empty') 

		outfile = self.getAvailableFileName( outfile )
		# if outfile already exists, we want to append numbers on the prefix
		self.outfile = outfile

	def getAvailableFileName(self,originalFile):

		count = 1
		file = originalFile
		while os.path.isfile( file ):
			fileName, fileExtension = os.path.splitext(originalFile)
			file = fileName + '.' + str(count) + fileExtension
			count += 1

		if file != originalFile:
			warnings.warn( "WARN: needed to change file to " + file )

		return file

	def append( self, entries ):

		writer = None

		# first time writing to the csv, we output the header
		if not os.path.isfile( self.outfile ):
			writer = self.csvWriter()
			writer.writerow( self.headers() )	
		else:
			writer = self.csvWriter()

		# for all fire entries
		for e in entries:
			writer.writerow( self.list(e) )

	def csvWriter(self):
		csvfile = open( self.outfile, 'ab')
		writer = unicodecsv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		return writer

	# we need to know the csv headers
	def headers(self):
		return [ 
			"POST_TITLE",
			"POST_DATE",
			"POST_LINK",

			"FIRE_DATE",
			"FIRE_TIME",
			"FIRE_TYPE",			
			"FIRE_ADDRESS",
			"FIRE_DETAILS"
		]

	# we need an ordered list to output to the csv
	def list(self, entry):

		return [ 
			entry.postTitle, 
			entry.postDate,
			entry.postLink,
			
			entry.fireDate,
			entry.fireTime,
			entry.fireType,
			entry.fireAddress, 
			entry.fireDetails
		]

