import re
import geopy
from geopy import *


class Geocoder:

	googleGeocoder = None

	def geocode(self, addressStr):

		return self.googleGeocode( addressStr )

	def googleGeocode( self, addressStr ):

		if self.googleGeocoder is None:
			self.googleGeocoder = geocoders.GoogleV3()


		testAddress = self.scrubAddress( addressStr )

		point = self.googleGeocoder.geocode( testAddress, timeout = 300 )

		if point is None:
			return None
		elif( point.latitude == 39.952335 ) and ( point.longitude == -75.163789 ):
			warnings.warn( "could not geocode '%s'" % testAddress )
		else:
			return point

	# take addressStr and return an address string that has the best chance of geocoding
	@staticmethod
	def scrubAddress( addressStr ):
		testAddress = Geocoder.stripLinks( addressStr )
		testAddress = Geocoder.stripBlockOf( testAddress )
		testAddress += ", Philadelphia PA"
		return testAddress

	# often times addresses contain " block of ", we're gonna strip that out
	@staticmethod
	def stripBlockOf( str ):
		return re.sub( '\s*block of\s*', ' ', str )

	# philly fire news sometimes has links in the address text	
	@staticmethod
	def stripLinks( str ):
		return re.sub( '<a.*>.*</a>','', str )

class GoogleGeocoder:


	def geocode( self, addressStr ):
		g = geocoders.GoogleV3()
		response = g.geocode( testAddress, timeout=300 ) 

		if response is not None:
			return response.point
		else:
			return None

