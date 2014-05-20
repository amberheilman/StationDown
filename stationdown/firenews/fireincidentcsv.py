from fire_incident import FireIncident
from StringIO import StringIO
import csv

class FireIncidentCSV:

	incidents = None

	def __init__(self, incidents):
		self.incidents = incidents

	def __str__(self):

		if self.incidents is None:
			self.incidents = FireIncident.objects.all()

		output = StringIO()
		writer = csv.writer(output,delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)

		# output csv header
		writer.writerow( ['fire_date','fire_type','fire_address','x','y','fire_details' ])

		for incident in self.incidents:
			writer.writerow( [
				incident.fireDateStr.encode( 'utf-8','ignore' ),
				incident.fireTypeStr.encode( 'utf-8','ignore' ),
				incident.fireAddressStr.encode( 'utf-8','ignore' ),
				str(incident.x).encode( 'utf-8','ignore' ),
				str(incident.y).encode( 'utf-8','ignore' ),
				incident.fireDetailsStr.encode( 'utf-8','ignore' )
			] )

		return output.getvalue()