#stationdown/firenews/scrape.py

from django.core.management.base import NoArgsCommand, BaseCommand, make_option

from stationdown.firenews.fireincidentsaver import FireIncidentSaver
from stationdown.firenews.fireincidentcsv import FireIncidentCSV
from stationdown.firenews.fire_incident import FireIncident

#
# set up a command that can be run as 'python manage.py scrape'
#
class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--save', action='store_true',help='scrape incidents and save them to the database'),
        make_option('--csv', action='store_true',help='output fire incidents in csv'),
    )

    def handle(self, *args, **options):
		save = options['save']

		if 'save' in options and options['save'] == True:

			fireNewsSaver = FireIncidentSaver()
			fireNewsSaver.save()

		elif 'csv' in options and options['csv'] == True:

			incidents = FireIncident.objects.all()
			csv = FireIncidentCSV(incidents)

			print csv