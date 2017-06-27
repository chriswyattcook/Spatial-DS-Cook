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

f = open(dir_path+"\\WorldData\\state_borders.json","r")

data = f.read()

data = json.loads(data)

all_states = []

for v in data:
    gj = collections.OrderedDict()

    gj['type'] = 'Feature'
    gj['properties'] = v
    gj['geometry'] = {}
    gj['geometry']['type'] = 'Polygon'
    gj['geometry']['coordinates'] = list(reversed(gj['properties']['borders']))
    del gj['properties']['borders']
    all_states.append(gj)

# pp.pprint(all_airports[0])

out = open(dir_path+"\\geo_json\\states_gj.geojson","w")

out.write(json.dumps(all_states, sort_keys=False,indent = 4, separators = (',',':')))

out.close()
