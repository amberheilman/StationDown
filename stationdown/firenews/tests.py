from django.test import TestCase

from stationdown.firenews.geocoder import *

class GeocoderTests(TestCase):

	def test_stripLinks(self):
		"""
		stripLinks() should return text that doesn't have any anchor link html, this includes not
		returning the text inside that link
		"""
		testAddress = 'Randolph and Venango St <a href="https://goo.gl/maps/bPQHO">Map</a>'
		expectedResult = 'Randolph and Venango St '
		g = Geocoder()
		result = g.stripLinks( testAddress )

		self.assertEqual(expectedResult, result)

		result = g.scrubAddress( testAddress )

	def test_scrubAddress(self):
		"""
		scrubAddress() should return text that doesn't have any anchor link html, this includes not
		returning the text inside that link
		"""
		testAddress = 'Randolph and Venango St <a href="https://goo.gl/maps/bPQHO">Map</a>'
		expectedResult = 'Randolph and Venango St '
		g = Geocoder()
		result = g.scrubAddress( testAddress )

		self.assertEqual(expectedResult, result)

		result = g.scrubAddress( testAddress )