'''[(u'Papumay', {'count': 1, 'coordinates': [-90.929862, 14.755234]})'''

from mongo_features_helper import *
from mapping_helper import *
import pprint as pp
import sys
import pygame
import operator

DIRPATH = os.path.dirname(os.path.realpath(__file__))

EPSILON = sys.float_info.epsilon  # smallest possible difference

#display
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)

#pygame stuff
pygame.init()
bg = pygame.image.load(DIRPATH+'/world_map.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('program_6: Global Terrorism')
screen.fill(background_colour)
pygame.display.flip()

#displays the pygame window with the background
screen.blit(bg, (0, 0))
pygame.display.flip()

#this is used to access the mongo db
mh = mongoHelper()

#separate all cities into a dictionary that only holds: city name, coordinates_of city, terrorism_count
all_cities_terror = {}

result_list = []

extremes = {}

extremes['max_x'] = width
extremes['min_x'] = 0
extremes['max_y'] = height
extremes['min_y'] = 0

#retrieves all the terrorist attacks
all_terror = mh.client['world_data']['terrorism'].find()

#fills all_cities_terror
for t in all_terror:
    if not t['properties']['city'] in all_cities_terror:
        all_cities_terror[t['properties']['city']] = {}
        all_cities_terror[t['properties']['city']]['count'] = 0 
        all_cities_terror[t['properties']['city']]['coordinates'] = (float(t['geometry']['coordinates'][0]),float(t['geometry']['coordinates'][1]))
    all_cities_terror[t['properties']['city']]['count'] += 1

#converts all lat,lon to x,y
for t in all_cities_terror:
    all_cities_terror[t]['coordinates'] = (mercX(all_cities_terror[t]['coordinates'][0]),mercY(all_cities_terror[t]['coordinates'][1])-256)

#gets rid of all_cities_terror['Unknown']
del all_cities_terror['Unknown']

#sorts based on number of attacks
sorted_cities = sorted(all_cities_terror.items(), key=lambda (k,v): v['count'])

#first item in sorted_cities is the largest
sorted_cities.reverse()

minval = (sorted_cities[-1][1]['count'])
maxval = (sorted_cities[0][1]['count'])

#https://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map
def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for sc in sorted_cities:
        pygame.draw.circle(screen, rgb(minval,maxval,sc[1]['count']), sc[1]['coordinates'], (sc[1]['count']//500),0)
        pygame.display.flip()

    pygame.image.save(screen, DIRPATH+'/program_6.png')