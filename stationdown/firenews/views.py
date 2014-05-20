from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.utils import simplejson
from django.core import serializers
import csv

from stationdown.firenews.fire_incident import FireIncident
from stationdown.firenews.fireincidentcsv import FireIncidentCSV

def fire_incidents(request):

	format = request.GET.get('format', None)
	all    = bool( request.GET.get('all', False) )

	# return because we're showing the map html
	if format is None:
		t = get_template('fire_incidents.html')
		html = t.render(Context())
		return HttpResponse(html)

	if all is True:
		incidents = FireIncident.objects.all()
	else:
		incidents = []
	
	if format == 'json':

		data = serializers.serialize("json", incidents )
		return HttpResponse( data, content_type="application/json")

	elif format == 'csv':

		csv = FireIncidentCSV( incidents )

		response = HttpResponse( csv, content_type="text/csv" )
		response['Content-Disposition'] = 'attachment; filename="fire_incidents.csv"'
		return response
