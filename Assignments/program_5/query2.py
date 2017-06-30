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
color_list = {'volcanos':(255,0,0),'earthquakes':(70,173,212),'meteorites':(76,187,23)}

#run db query for next airport within the r
#find all vol as red, eq as blue, meteor as green
#repeat steps until at end_pt

pygame.init()
bg = pygame.image.load(DIRPATH+'/world_map.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('query1')
screen.fill(background_colour)
pygame.display.flip()

#sets all variables to None
feature = None
field = None
field_value = None
min_max = None
max_results = None
radius = None
lat,lon = (None,None)

#sys.argv loaded into variables
#defaults if nothing is after query2.py
if(len(sys.argv)==1):
    radius = 200
    max_results = 100
#if only a radius is passed in (will use mouse input)
elif(len(sys.argv)>1 and (len(sys.argv))<3):
    radius = float(sys.argv[1])
    max_results = 100
#if everything is passed in except a lat,lon (will use mouse input)
elif(len(sys.argv)>3):
    #separates argv
    feature = sys.argv[1]
    field = sys.argv[2]
    field_value = float(sys.argv[3])
    min_max = sys.argv[4]
    max_results = int(sys.argv[5])
    radius = float(sys.argv[6])
    #if a lat,lon is passed in (will not use mouse input)
    if(len(sys.argv) > 7):
        lat,lon = eval(sys.argv[7])

mh = mongoHelper()

#variables used in the game loop
x_y_coords = None
result_list = []
res = []
feature_list = ['volcanos','earthquakes','meteorites']

#these are used to convert lon,lat to x,y
allx = []
ally = []
points = []
extremes = {}
adj = {}

#flags to trigger certain parts of the code
picked_pt = False
if(len(sys.argv))>7:
    picked_pt = True
converted_to_lat_lon = False
find_feature = True
drawn = False

running = True
while running:
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    #pygame.image.save(screen, DIRPATH+'/query1.png')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and (len(sys.argv) < 3) and picked_pt == False:
            x_y_coords = (event.pos[0],event.pos[1])
            picked_pt = True
    
    #convert x_y_coords to lat,lon for mongodb
    if x_y_coords != None and converted_to_lat_lon == False:
        #Dont have a way to conert this yet
        #lat,lon = print("gon' convert this bitch", x_y_coords)
        lat, lon = (event.pos[0],event.pos[1])
        converted_to_lat_lon = True



    if picked_pt == True and find_feature == True:
        if feature == None:
            adj = {'volcanos':None,'earthquakes':None,'meteorites':None}
            for f in feature_list:
                result_list = mh.get_features_near_me(f,(lon,lat),radius)
                
                extremes,points = find_extremes(result_list)

                adj[f] = (adjust_location_coords(extremes,points,width,height))
                
                
        else:
            print(lon,lat)
            result_list = mh.get_features_near_me(feature,(lon,lat),radius)
            adj = {feature: None}
            for r in result_list:
                if min_max == 'min':
                    if float(r['properties'][field]) > field_value:
                        res.append(r)
                if min_max == 'max':
                    if r['properties.'+field] < field_value:
                        res.append(r)
            result_list = []
            for f in range(max_results):
                result_list.append(res[f])

            extremes,points = find_extremes(result_list)

            adj[feature] = (adjust_location_coords(extremes,points,width,height))

        pp.pprint(result_list)
        find_feature = False
        pp.pprint(adj)

    if picked_pt == True and drawn == False:
        for f in adj.keys():
            for pt in adj[f]:
                print(color_list[f],pt)
                pygame.draw.circle(screen, color_list[f], pt, 2,1)
                pygame.display.flip()
        pygame.image.save(screen, DIRPATH+'/query2.png')
        drawn = True 
        
    
        