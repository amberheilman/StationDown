from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.core import serializers
import csv

from stationdown.firestations.facility import Facility

def stations_get(request):

    stations = Facility.objects.all()
    
    for s in stations:
        s.x = s.point.x
        s.y = s.point.y

    data = serializers.serialize("json", stations )
    return HttpResponse( data, content_type="application/json")