from mongo_helper_class import *
from pygame_helper import *
import pprint as pp
import sys
import pygame


DIRPATH = os.path.dirname(os.path.realpath(__file__))

picked_pt = False

#checks if argv will be used. Otherwise, defaults to DFW MNL 500
if(len(sys.argv) > 1):    
    start_pt = sys.argv[1]
    end_pt = sys.argv[2]
    r = float(sys.argv[3])
    picked_pt = True

#display
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)
color_list = {'volcanos':(255,0,0),'earthquakes':(70,173,212),'meteorites':(76,187,23)}
box_color = (255,255,0)

pygame.init()
bg = pygame.image.load(DIRPATH+'/world_map.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('query1')
screen.fill(background_colour)
pygame.display.flip()

mh = mongoHelper()

screen.blit(bg, (0, 0))
pygame.display.flip()

#get coords of start,end
start =  mh.get_doc_by_keyword('airports','ap_iata',start_pt)
start_coords = mh.get_coordinates(start[0])

end =  mh.get_doc_by_keyword('airports','ap_iata',end_pt)
end_coords = mh.get_coordinates(end[1]) 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and picked_pt = False:
            start_pt = (event.pos[0],event.pos[1])
            end_pt = (event.pos[0],event.pos[1])
            #convert pt to coords
            r = 500
            picked_pt = True

    #run db query for next airport within the r
    #use haversine formula to find the airport within r that is closest to the end_pt
    #find all vol as red, eq as blue, meteor as green within r
    #store in {}
    #store airport points in a list
    #repeat steps until at end_pt

    #draw lines (query3)
    #draw dots (like query2)
    

  