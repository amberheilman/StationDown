from stationdown.settings import *

# Test runner with no database creation
TEST_RUNNER = 'stationdown.scripts.testrunner.NoDbTestRunner'

INSTALLED_APPS = (
    #'django.contrib.admin',
    ##'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stationdown',
    'stationdown.firenews',
)