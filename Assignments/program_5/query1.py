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

pygame.init()
bg = pygame.image.load(DIRPATH+'/world_map.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('query1: Finding Features')
screen.fill(background_colour)
pygame.display.flip()

picked_pt1 = False
picked_pt2 = False
converted_to_x_y = False
radius = 500
start_coords = None
end_coords = None
done = False
closest = None
distance = 9999999
pt_list = []
res = []
feature_list = ['volcanos','earthquakes','meteorites']
#these are used to convert lon,lat to x,y
allx = []
ally = []
points = []
extremes = {}
adj = {}

extremes['max_x'] = width
extremes['min_x'] = 0
extremes['max_y'] = height
extremes['min_y'] = 0

#checks if argv will be used
if(len(sys.argv) > 1):    
    start_pt = sys.argv[1]
    end_pt = sys.argv[2]
    radius = float(sys.argv[3])
    picked_pt1 = True
    picked_pt2 = True

    #get coords of start,end
    start =  mh.get_doc_by_keyword('airports','ap_iata',start_pt)
    start_coords = mh.get_coordinates(start[0])

    end =  mh.get_doc_by_keyword('airports','ap_iata',end_pt)
    end_coords = mh.get_coordinates(end[1]) 



mh = mongoHelper()

screen.blit(bg, (0, 0))
pygame.display.flip()

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
                pt_list.append(end_coords)
                done = True


    if converted_to_x_y == False and done == True:
        for pt in pt_list:
            adj = {'volcanos':None,'earthquakes':None,'meteorites':None}
            for f in feature_list:
                result_list = mh.get_features_near_me(f,(lon,lat),radius)
                
                extremes,points = find_extremes(result_list, width, height)

                adj[f] = (adjust_location_coords(extremes,points,width,height))
            x = mercX(pt[1])
            y = mercY(pt[0])
            res.append((x,y))
        adj['airports'] = adjust_location_coords(extremes,res,width,height)
        converted_to_x_y = True
    if converted_to_x_y == True and done == True:
        #print(adj)
        for f in adj.keys():
            for pt in adj[f]:
                pygame.draw.circle(screen, color_list[f], pt, 2,1)
                pygame.display.flip()
        pygame.draw.lines(screen, (255,0,255), False, adj['airports'])
        pygame.image.save(screen, DIRPATH+'/query1.png')