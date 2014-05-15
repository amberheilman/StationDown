

import os
import sys

sys.path.append('/home/jsmiley/Documents/Development/StationDown')
sys.path.append('/home/jsmiley/Documents/Development/StationDown/stationdown')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stationdown.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.core.wsgi import get_wsgi_application
from dj_static import Cling


application = Cling(get_wsgi_application())
