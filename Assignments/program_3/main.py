import requests
import json
import sys
import glob
import math
import os
import pygame
import time

DIRPATH = os.path.dirname(os.path.realpath(__file__))

def condense_file(data):
    condensed_data = []

    for quake in data['features']:
        keep = {}
        keep['geometry'] = quake['geometry']
        keep['mag'] = quake["properties"]["mag"]
        keep['magType'] = quake["properties"]["magType"]
        keep['time'] = quake["properties"]["time"]
        keep['place'] = quake["properties"]["place"]
        keep['types'] = quake["properties"]["types"]
        keep['rms'] = quake["properties"]["rms"]
        keep['sig'] = quake["properties"]["sig"]
        condensed_data.append(keep)

    return condensed_data
    

##########################################################################################

def get_earth_quake_data(year=[1960,1960],month=[1,12],minmag=None,maxmag=None,query=True):
    start_year = year[0]
    end_year = year[1]
    start_month = month[0]
    end_month = month[1]

    if not maxmag is None:
        maxmag = '&maxmagnitude='+str(maxmag)
    else:
        maxmag = ''

    if not minmag is None:
        minmag = '&minmagnitude='+str(minmag)
    else:
        minmag = '&minmagnitude='+str(1.0)

    if query:
        type = 'query'

    else:
        type = 'count'

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/'+type+'?format=geojson&starttime='+str(start_year)+'-'+str(start_month)+'-01&endtime='+str(end_year)+'-'+str(end_month)+'-01'+minmag+maxmag

    r = requests.get(url).json()

    if type == 'count':
        return r['count']
    else:
        return r

def mercX(lon):
    """
    Mercator projection from longitude to X coord
    """
    zoom = 1.0
    lon = math.radians(lon)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = lon + math.pi
    return int(a * b)


def mercY(lat):
    """
    Mercator projection from latitude to Y coord
    """
    zoom = 1.0
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return int(a * c)

def adjust_location_coords(extremes,points,width,height):
    """
    Adjust your point data to fit in the screen. 
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    maxx = float(extremes['max_x']) # The max coords from bounding rectangles
    minx = float(extremes['min_x'])
    maxy = float(extremes['max_y'])
    miny = float(extremes['min_y'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted = []

    for p in points:
        x,y = p
        x = float(x)
        y = float(y)
        xprime = (x - minx) / deltax         # val (0,1)
        yprime = ((y - miny) / deltay) # val (0,1)
        adjx = int(xprime*width)
        adjy = int(yprime*height)
        adjusted.append((adjx,adjy))
    return adjusted

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)


path = '/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/EarthquakeData'
years = [x for x in range(1960,2017)]
months = [x for x in range(0,12)]

r = get_earth_quake_data([1960,2016],[1,12],7,None,True)
f = open('./quake-1960-2017-7.json','w')
f.write(json.dumps(r, sort_keys=True,indent=4, separators=(',', ': ')))
f.close()
rc = condense_file(r)
f = open('./quake-1960-2017-7-condensed.json','w')
f.write(json.dumps(rc, sort_keys=True,indent=4, separators=(',', ': ')))
f.close()

# Open our condensed json file to extract points
f = open(DIRPATH+'/quake-1960-2017-7-condensed.json','r')
data = json.loads(f.read())

allx = []
ally = []
points = []

# Loop through converting lat/lon to x/y and saving extreme values. 
for quake in data:
    #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    lon = quake['geometry']['coordinates'][0]
    lat = quake['geometry']['coordinates'][1]
    x,y = (mercX(lon),mercY(lat))
    allx.append(x)
    ally.append(y)
    points.append((x,y))

# Create dictionary to send to adjust method
extremes = {}
extremes['max_x'] = max(allx)
extremes['min_x'] = min(allx)
extremes['max_y'] = max(ally)
extremes['min_y'] = min(ally)

# Get adjusted points
screen_width = 1024
screen_height = 512
adj = adjust_location_coords(extremes,points,screen_width,screen_height)

# Save adjusted points
f = open('./quake-1960-2017-7-adjusted.json','w')
f.write(json.dumps(adj, sort_keys=True,indent=4, separators=(',', ': ')))
f.close()

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)

pygame.init()
# Put this after pygame.init()
bg = pygame.image.load(DIRPATH+'/world_map.png')

screen = pygame.display.set_mode((width, height))



screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('7.0+ Earthquakes: 1960 - 2016')
screen.fill(background_colour)

pygame.display.flip()
f = open(DIRPATH+'/quake-1960-2017-7-adjusted.json','r')
points = json.loads(f.read())

running = True
while running:
    screen.blit(bg, (0, 0))

    for p in points:
        pygame.draw.circle(screen, (70,173,212), p, 2,1)
        pygame.display.flip()
        time.sleep(0.01)
    
    pygame.image.save(screen, DIRPATH+'/7.0_quakes_1960-2016.png')
    input()

    #pygame.image.save(screen , DIRPATH+'/7.0_quakes_1960-2016.png')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False