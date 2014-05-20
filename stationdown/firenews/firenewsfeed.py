import requests
import feedparser
from fire_incident import *

class FireNewsFeed:

	done = False
	pageNum = None

	# head to the site and return the xml feed pages as strings
	def fetchNextPage(self,justOnePage = False):

		if self.pageNum is None:
			self.pageNum = 1
		else:
			self.pageNum += 1

		fireIncidentsList = []

		print "retreiving page " + str(self.pageNum) + " from Philly Fire News feed"

		url = self.url( self.pageNum ) 
		response = requests.get(url, allow_redirects=False)
		responseCode = response.status_code
		xmlStr = response.text

		if responseCode == 200:
			# add on the list returned to fireIncidentsList
			fireIncidentsList.extend( self.parseXmlPage(xmlStr) )
		else:
			self.done = True

		#set second boolean to false if you just want to check a 1 page download
		if self.pageNum > 1 and justOnePage:
			self.done = True

		return fireIncidentsList

	# given the page number return the url that we would use to
	# retreive it
	@staticmethod
	def url( pageNum ):
	
		# we've disabled follow redirects so if you pass page = 1, 
		# it will try to redirect to general feed/
		# so if page = 1, we need to give it the general feed url
		if pageNum == 1:
			return "http://www.phillyfirenews.com/category/fire_wire/pennsylvania/city-of-philadelphia/feed/"
		else:
			return "http://www.phillyfirenews.com/category/fire_wire/pennsylvania/city-of-philadelphia/feed/?paged=" + str(pageNum)

	# return true if there's still another page available to retreive
	def hasNext(self):
		return not self.done;

	# get the current page number
	def getCurrentPageNum( self ):
		return self.pageNum

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