from django.contrib.gis.db import models
import re
#
# FeedEntry is a container for the information stored in each Philly Fire News post
#
class FireIncident(models.Model):

	id = models.AutoField(primary_key=True)

	postTitleStr = models.CharField(max_length=255,blank=False)
	postLinkStr  = models.CharField(max_length=255,blank=False)
	postDateStr  = models.CharField(max_length=255,blank=False)
	
	fireDateStr = models.CharField(max_length=255,blank=False)
	fireTimeStr = models.CharField(max_length=255)
	fireAddressRaw = models.TextField()
	fireAddressStr = models.TextField()
	fireTypeStr = models.CharField(max_length=255)
	fireDetailsStr = models.TextField()
	
	point = models.PointField()
		
	x = models.FloatField()
	y = models.FloatField()

	def __str__(self):
		return "{date}, {address} {x} {y}".format(
			date=self.fireDateStr, address=self.fireAddressStr, 
					x=self.point.coords[0], y=self.point.coords[1] )


class FireIncidentManager(models.Manager):

	def create_feed_entry( self, dataList ):
		feedEntry = FireIncident()
		feedEntry.postTitleStr = dataList.title.encode( 'utf-8','replace' )
		feedEntry.postLinkStr  = dataList.link.encode( 'utf-8','replace' )
		feedEntry.postDateStr  = dataList.published.encode( 'utf-8','replace' )
		
		contentObj = PostContentHtml( dataList.content )
		
		feedEntry.fireDateStr = contentObj.fireDate.encode( 'utf-8','replace' )
		feedEntry.fireTimeStr = contentObj.fireTime.encode( 'utf-8','replace' )
		feedEntry.fireAddressRaw = contentObj.fireAddress.encode( 'utf-8','replace' )
		feedEntry.fireAddressStr = self.scrubAddress( feedEntry.fireAddressRaw )
		feedEntry.fireTypeStr = contentObj.fireType.encode( 'utf-8','replace' )
		feedEntry.fireDetailsStr = contentObj.fireDetails.encode( 'utf-8','replace' )

		return feedEntry

	# take addressStr and return an address string that has the best chance of geocoding
	@staticmethod
	def scrubAddress( addressStr ):
		
		if addressStr is None:
			raise Exception( 'addressStr may not be None' )
			
		testAddress = FireIncidentManager.stripLinks( addressStr )
		testAddress = FireIncidentManager.stripBlockOf( testAddress )

		return testAddress

	# often times addresses contain " block of ", we're gonna strip that out
	@staticmethod
	def stripBlockOf( str ):
		return re.sub( '\s*block of\s*', ' ', str )

	# philly fire news sometimes has links in the address text	
	@staticmethod
	def stripLinks( str ):
		return re.sub( '<a.*>.*</a>','', str )
		
#
# PostContentHtml is the container and parser for the fire details contained in the wordpress post html
#
class PostContentHtml:
	
	# feedparser fills entry.content with a list, be prepared for it
	def __init__( self, contentList ):

		# feedparser puts content into a list because atom feeds may have multiples, 
		# we need a string
		contentStr = self.listToString( contentList )

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

