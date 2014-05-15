from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

def home(request):
	t = get_template('home.html');
	return HttpResponse( t.render( Context()));

def fire_stations(request):
	t = get_template('fire_stations.html')
	html = t.render(Context())
	return HttpResponse(html)