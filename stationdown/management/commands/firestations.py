#stationdown/firenews/scrape.py

from django.core.management.base import NoArgsCommand, BaseCommand, make_option

from stationdown.firestations.facility import Facility
from stationdown.firenews.fire_incident import FireIncident
from stationdown.firestations.closeststationfinder import ClosestStationFinder

#
# set up a command that can be run as 'python manage.py scrape'
#
class Command(NoArgsCommand):

    def handle(self, *args, **options):
        incidents = FireIncident.objects.all()

        closestStationFinder = ClosestStationFinder()

        for incident in incidents:
            closestStationFinder.getClosestStation( incident )

