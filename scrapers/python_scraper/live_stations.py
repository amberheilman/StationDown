import csv
import time

def remove_Brownouts(all_Stations, closed_Stations, timestamp):
    print(time)
    allrdr = csv.reader(open(all_Stations))
    closedrdr = csv.reader(open(closed_Stations))
    for station in closedrdr:
        print(station[2])#, station[3], station[4], station[7], station[8], station[9])
        if station[2] in allrdr:
            print(station)
         
remove_Brownouts('fire_locations.csv', 'fire_data.csv', time)
