Fire News Python Module
=======================

The purpose of this module is to interact with the website Philly Fire News and pull down the fire incidents that it's tracking

the command:

python manage.py firenews --save

will retreive the entries and store it in the Postgres database

the command:

python manage.py firenews --geocode

will geocode those entries and create entries in a new table

To initialize the databse, you run:

python manage.py syncdb