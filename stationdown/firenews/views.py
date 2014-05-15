from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

def fire_incidents(request):
	t = get_template('fire_incidents.html')
	html = t.render(Context())
	return HttpResponse(html)
