# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stationdown_dev',                      
        'USER': 'stationdown_dev',
        'PASSWORD': '',
        'HOST': 'spruce.phl.io'
    }
}