import re
import geopy
from geopy import *


class Geocoder:

	googleGeocoder = None

	def geocode(self, addressStr):
		
		if addressStr is None:
			raise Exception( 'addressStr may not be None' )

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



class GoogleGeocoder:


	def geocode( self, addressStr ):
		g = geocoders.GoogleV3()
		response = g.geocode( testAddress, timeout=300 ) 

		if response is not None:
			return response.point
		else:
			return None

