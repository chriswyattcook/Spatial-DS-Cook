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

f = open(dir_path+"\\WorldData\\world_cities_large.json","r")

data = f.read()

data = json.loads(data)

all_cities = []

for k,v in data.items():
    for c in v:
        gj = collections.OrderedDict()

        gj['type'] = 'Feature'
        gj['properties'] = c
        lat = c['lat']
        lon = c['lon']
        del gj['properties']['lat']
        del gj['properties']['lon']
        gj['geometry'] = {}
        gj['geometry']['type'] = 'Point'
        gj['geometry']['coordinates'] = [float(lon),float(lat)]
        all_cities.append(gj)

out = open(dir_path+"\\geo_json\\world_cities_gj.geojson","w")

out.write(json.dumps(all_cities, sort_keys=False,indent = 4, separators = (',',':')))

out.close()
