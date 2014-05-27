import time
import operator
from google.directions import GoogleDirections

from stationdown.firenews.fire_incident import *
from facility import *

class ClosestStationFinder:

    stations = None

    def __init__(self):
        pass

    def getClosestStation(self, incident ):

        stations = self.getStations()

        counter = 0
        for s in stations:
            seconds = self.getDuration(incident.point, s.point)
            s.duration = seconds
            print str(counter) + " " + str(seconds)
            counter += 1
            time.sleep(.125) # through trial and error .125 seconds seems good, .0625 gives quota status err

        # sort the stations by duration
        stations = sorted(stations, key=operator.attrgetter('duration') )

        print "lowest station: " + stations[0].locationStr + " duration: " + str(stations[0].duration)

        return stations[0]

    # return a list of stations
    def getStations(self):

        if self.stations is None:
            self.stations = Facility.objects.all()

        return self.stations

    def getDirections( self, startPoint, endPoint ):

        startX = startPoint.x
        startY = startPoint.y
        endX   = endPoint.x
        endY   = endPoint.y
         
        gd = GoogleDirections('AIzaSyCUyKgIqRsJcdjrmOHDKJSBgyaBwDvfkbw')
        response = gd.query( "{1},{0}".format(startX,startY), "{1},{0}".format(endX,endY) )

        status = response.status

        if status == 620:
            raise Exception('status 604: Google thinks you\'re geocoding too fast')
        elif status != 200:
            raise Exception( "received status {status}; unable to geocode from:{sY},{sX} to:{eY},{eX}".format(status=status,
                sY=startY,sX=startX,
                eY=endY,eX=endX) 
            )

        return response.result

    # return the duration of the trip from fromPoint to toPoint in seconds
    def getDuration( self, fromPoint, toPoint ):
        result = self.getDirections( fromPoint.x, fromPoint.y, toPoint.x, toPoint.y )
        return result['Directions']['Duration']['seconds']
