# stationdown/database_local.py
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'stationdown_dev',                      
        'USER': 'stationdown_dev',
        'PASSWORD': 'Password123',
        'HOST': 'spruce.phl.io'
    }
}
