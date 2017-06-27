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

f = open(dir_path+"\\WorldData\\world_volcanos.json","r")

data = f.read()

data = json.loads(data)

all_volcanos = []

for v in data:
    gj = collections.OrderedDict()

    gj['type'] = 'Feature'
    gj['properties'] = v
    lat = v['Lat']
    lon = v['Lon']
    del gj['properties']['Lat']
    del gj['properties']['Lon']
    gj['geometry'] = {}
    gj['geometry']['type'] = 'Point'
    if lon != "":
        lon = float(lon)
    if lat != "":
        lat = float(lat)
    gj['geometry']['coordinates'] = [lon,lat]
    all_volcanos.append(gj)

# pp.pprint(all_volcanos[0])

out = open(dir_path+"\\geo_json\\volcanos_gj.geojson","w")

out.write(json.dumps(all_volcanos, sort_keys=False,indent = 4, separators = (',',':')))

out.close()
