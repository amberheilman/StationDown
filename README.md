StationDown
===========

[http://stationdown.herokuapp.com](http://stationdown.herokuapp.com)

Every day, the Philadelphia Fire Department closes fire stations and relocates staff to other stations. This endangers citizens by overwhelming ajoining stations and stretching resources, leading to longer response times.

This application will map the fire stations in Philadelphia and indicate if they are closed, alongside fire indicents that occur throughout the day provided by phillyfirenews.com. 

In the future, the trip of the responding station will be calculated and compared to the closed station in order to find if the response time was adversely affected by the station brown out.

Brown out: "It is when you take an engine or ladder company out of service temporarily and re-distribute the staff for either training or to fill in personnel gaps in other companies." -http://www.phila.gov/fire/pdfs/Brown-Out_FAQ.pdf

A list of Philadelphia fire incidents can be found [here](http://stationdown.herokuapp.com/fire-incidents/list)

### Fire Station Brownout Closing Schedule

Here is the repository of PDFs containing the schedule

https://github.com/jimRsmiley/phila-fire-station-brownout-schedule-pdfs

### Scraping Fire Locations from Philly Fire News

The firenews app under stationdown handles interacting with the [http://phillyfirenews.com](Philly Fire News website) to pull down fire incidents. [Read more here](stationdown/firenews/README.md)

To pull down the fire incidents and save them into postGIS, run: 'python manage.py save'

### Fusion Table of Fire Stations

A fusion table of Philadelphia fire stations is located 
[here](https://www.google.com/fusiontables/embedviz?q=select+col3+from+1HY9mXeOfgIZ4GYv5gUaI4zi6xPlafyPrFWA7dwU&viz=MAP&h=false&lat=39.95709485745125&lng=-75.10653457187499&t=1&z=11&l=col3&y=2&tmplt=3&hml=GEOCODABLEG).

### Download and Install

Station Down is written in Python 2.7.6 with the Django Framework and GeoDjango GIS module.

<pre><code>
git clone https://github.com/amberheilman/StationDown.git

cd StationDown

virtualenv --no-site-packages venv

source venv/bin/activate

pip install -r requirements.txt
</code></pre>
