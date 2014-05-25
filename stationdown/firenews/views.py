from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.utils import simplejson
from django.core import serializers
import csv

from stationdown.firenews.fire_incident import FireIncident
from stationdown.firenews.fireincidentcsv import FireIncidentCSV

def fire_home(request):
	t = get_template('fire_home.html')
	html = t.render(Context())
	return HttpResponse(html)

def fire_csv(request):
	incidents = FireIncident.objects.all()
	csv = FireIncidentCSV( incidents )

	response = HttpResponse( csv, content_type="text/csv" )
	response['Content-Disposition'] = 'attachment; filename="fire_incidents.csv"'
	return response

def fire_show(request):

	format = request.GET.get('format', None)
	all    = bool( request.GET.get('all', False) )

	# return because we're showing the map html
	if format is None:
		t = get_template('show.html')
		html = t.render(Context())
		return HttpResponse(html)

	if all is True:
		incidents = FireIncident.objects.all()
	else:
		incidents = []
	
	if format == 'json':

		data = serializers.serialize("json", incidents )
		return HttpResponse( data, content_type="application/json")

		

def fire_list(request):
	incidents = FireIncident.objects.all()

	t = get_template('list.html')
	html = t.render(Context({"incidents":incidents,"test":"test"}))
	return HttpResponse(html)

	

