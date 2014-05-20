import csv
import httplib2
import json
import time


def get_stations(url):
    h = httplib2.Http(".cache")
    (resp, content) = h.request(url, "GET")
    write_json(content)

def write_json(content):
    with open('fire_stations.txt', 'w') as outfile:
        json.dump(content, outfile)

def remove_Brownouts(all_Stations, closed_Stations, timestamp):
    print(time)
    allrdr = csv.reader(open(all_Stations))
    closedrdr = csv.reader(open(closed_Stations))
    for station in closedrdr:
        print(station[2])#, station[3], station[4], station[7], station[8], station[9])
        if station[2] in allrdr:
            print(station)

#remove_Brownouts('fire_locations.csv', 'fire_data.csv', time)

get_stations("http://gis.phila.gov/arcgis/rest/services/PhilaGov/Fire_Stations/MapServer/1/query?where=OBJECTID+%3E%3D+0&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=OBJECTID%2C+FIRESTA_%2C+ENG%2C+LAD%2C+BC%2C+MED%2C+SPCL%2C+SPCL3%2C+SPCL3%2C+LOCATION%2C+RAD%2C+ACTIVE%2C+SHAPE&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=pjson")
