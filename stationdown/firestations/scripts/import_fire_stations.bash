#!/bin/bash

PG_HOST=spruce.phl.io
PG_USER=postgres
DB_NAME=stationdown_dev
TABLE_NAME=fire_dept_facilities
SHAPEFILE=../../../data/Philadelphia_Fire_Dept_Facilities201302/Philadelphia_Fire_Dept_Facilities201302/Philadelphia_Fire_Dept_Facilities201302.shp

if [ -z "$STATIONDOWN_PG_PASS" ]
then
  echo 'must set postgres user pass with STATIONDOWN_PG_PASS'
  exit
fi

if [ ! -f $SHAPEFILE ]
then
  echo "shapefile $SHAPEFILE does not exist"
  exit
fi

# overwrite the table and transform to latitude and longitude
cmd='ogr2ogr -overwrite -t_srs EPSG:4326'

dest="\"PostgreSQL\" PG:\"host=$PG_HOST user=$PG_USER dbname=$DB_NAME password=$STATIONDOWN_PG_PASS\""

full="$cmd -f $dest -nln $TABLE_NAME $SHAPEFILE"

echo $full

eval $full
