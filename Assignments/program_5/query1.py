"""
Program:
--------
    Program 5 - query1 : Finding Features

Description:
------------
    See README
    
Name: Chris W Cook
Date: 05 July 2017
"""
from mongo_features_helper import *
from mapping_helper import *
import pprint as pp
import sys
import pygame

DIRPATH = os.path.dirname(os.path.realpath(__file__))

#display
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)
color_list = {'airports': (255,0,255),'volcanos':(255,0,0),'earthquakes':(70,173,212),'meteorites':(76,187,23),}
box_color = (255,255,0)

#pygame stuff
pygame.init()
bg = pygame.image.load(DIRPATH+'/world_map.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('query1: Finding Features')
screen.fill(background_colour)
pygame.display.flip()

#flags used in the running loop
picked_pt1 = False
picked_pt2 = False
converted_to_x_y = False
done = False

#defaults
radius = 500
start_coords = None
end_coords = None
closest = None
distance = 9999999

#these are used to store various pts,
pt_list = []
res = []
airports = []

#these are used to convert lon,lat to x,y
allx = []
ally = []
points = []
extremes = {}

#these are used to store features
feature_list = ['volcanos','earthquakes','meteorites']
adj = {'volcanos':None,'earthquakes':None,'meteorites':None}

#checks if argv will be used
if(len(sys.argv) > 1):    
    start_pt = sys.argv[1]
    end_pt = sys.argv[2]
    radius = float(sys.argv[3])
    picked_pt1 = True
    picked_pt2 = True

    #get coords of start,end
    start =  mh.get_doc_by_keyword('airports','properties.ap_iata',start_pt)
    start_coords = (start[0]['geometry']['coordinates'][1],start[0]['geometry']['coordinates'][0])
    pt_list.append(start_coords)

    end =  mh.get_doc_by_keyword('airports','properties.ap_iata',end_pt)
    end_coords = (end[0]['geometry']['coordinates'][1],end[0]['geometry']['coordinates'][0])


#this is used to access the mongo db
mh = mongoHelper()

#displays the pygame window with the background
screen.blit(bg, (0, 0))
pygame.display.flip()

#game loop
running = True
while running:
    pygame.event.pump()
    event = pygame.event.wait()
    button = pygame.mouse.get_pressed()
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN and button[0] == True and picked_pt1 == False:
        start_coords = (y_to_lat(event.pos[1],height),x_to_lon(event.pos[0],width))
        pt_list.append(start_coords)
        picked_pt1 = True
    if event.type == pygame.MOUSEBUTTONDOWN and button[2] == True and picked_pt2 == False:
        end_coords = (y_to_lat(event.pos[1],height),x_to_lon(event.pos[0],width))
        picked_pt2 = True

    #finds the list of airports that connect the start and the end
    if picked_pt1 == True and picked_pt2 == True and done == False:
        while done == False:
            result_list = mh.get_features_near_me('airports',(start_coords[1],start_coords[0]),int(radius))
            for r in result_list:
                lon = r['geometry']['coordinates'][0]
                lat = r['geometry']['coordinates'][1]
                d = mh._haversine(lon,lat,end_coords[1],end_coords[0])
                if d < distance:
                    closest = (lat,lon)
                    distance = d
            pt_list.append(closest)
            start_coords = closest
            if(mh._haversine(start_coords[1],start_coords[0],end_coords[1],end_coords[0])<radius):
                done = True

    #converts all airport pts to (x,y)
    if converted_to_x_y == False and done == True:
        pt_list.append(end_coords)
        for pt in pt_list:
            x = mercX(pt[1])
            y = mercY(pt[0])
            res.append((x,y))
        airports = adjust_location_coords(extremes,res,width,height)
        converted_to_x_y = True

    #prints all feature pts, airport pts, and draws lines connecting the airports
    if converted_to_x_y == True and done == True:
        for pt in pt_list:
            for f in feature_list:
                result_list = mh.get_features_near_me(f,(pt[1],pt[0]),radius)
                extremes,points = find_extremes(result_list, width, height)
                adj[f] = (adjust_location_coords(extremes,points,width,height))
                for ppt in adj[f]:
                    pygame.draw.circle(screen, color_list[f], ppt, 2,1)
                    pygame.display.flip()
        pygame.draw.lines(screen, (255,0,255), False, airports)
        #saves the final image
        pygame.image.save(screen, DIRPATH+'/query1.png')