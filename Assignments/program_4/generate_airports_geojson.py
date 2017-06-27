"""
Program:
--------
    Program 4 - Generating geo json from json files

Description:
------------
    This program reads in a particular json file and converts it to a geo json format.
    
Name: Chris W Cook
Date: 28 June 2017
"""
import pprint as pp
import os,sys
import json
import collections

dir_path = os.path.dirname(os.path.realpath(__file__))

f = open(dir_path+"\\WorldData\\airports.json","r")

data = f.read()

data = json.loads(data)

all_airports = []

for k,v in data.items():
    gj = collections.OrderedDict()

    gj['type'] = 'Feature'
    gj['properties'] = v
    lat = v['lat']
    lon = v['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']
    gj['geometry'] = {}
    gj['geometry']['type'] = 'Point'
    gj['geometry']['coordinates'] = [lon,lat]
    all_airports.append(gj)

# pp.pprint(all_airports[0])

out = open(dir_path+"\\geo_json\\airports_gj.geojson","w")

out.write(json.dumps(all_airports, sort_keys=False,indent = 4, separators = (',',':')))

out.close()
