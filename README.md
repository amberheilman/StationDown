StationDown
===========

Every day, the Philadelphia Fire Department closes fire stations and relocates staff to other stations. This endangers citizens by overwhelming ajoining stations and stretching resources, leading to longer response times.

This application will map the fire stations in Philadelphia and indicate if they are closed, alongside fire indicents that occur throughout the day provided by phillyfirenews.com. 

In the future, the trip of the responding station will be calculated and compared to the closed station in order to find if the response time was adversely affected by the station brown out.

Brown out: "It is when you take an engine or ladder company out of service temporarily and re-distribute the staff for either training or to fill in personnel gaps in other companies." -http://www.phila.gov/fire/pdfs/Brown-Out_FAQ.pdf


Scraping Fire Locations from Philly Fire News
=========================
Run the command 'python manage.py scrape'

Fusion Table of Fire Stations:
https://www.google.com/fusiontables/embedviz?q=select+col3+from+1HY9mXeOfgIZ4GYv5gUaI4zi6xPlafyPrFWA7dwU&viz=MAP&h=false&lat=39.95709485745125&lng=-75.10653457187499&t=1&z=11&l=col3&y=2&tmplt=3&hml=GEOCODABLEG

http://stationdown.herokuapp.com
