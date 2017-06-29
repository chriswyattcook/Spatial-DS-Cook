from mongo_helper_class import *
from pygame_helper import *
import pprint as pp
import sys
import pygame


DIRPATH = os.path.dirname(os.path.realpath(__file__))

#checks if argv will be used. Otherwise, defaults to DFW MNL 500
try:    
    start_pt = sys.argv[1]
    end_pt = sys.argv[2]
    r = float(sys.argv[3])
except:
    start_pt = 'DFW'
    end_pt = "MNL"
    r = 500

#run db query for next airport within the r
#find all vol as red, eq as blue, meteor as green
#repeat steps until at end_pt
mh = mongoHelper()

#get coords of start,end
start =  mh.get_doc_by_keyword('airports','ap_iata',start_pt)
start_coords = mh.get_coordinates(start[0])

end =  mh.get_doc_by_keyword('airports','ap_iata',end_pt)
end_coords = mh.get_coordinates(end[1])      
    

#display
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)

pygame.init()
bg = pygame.image.load(DIRPATH+'/world_map.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('query1')
screen.fill(background_colour)
pygame.display.flip()

running = True
while running:
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    #pygame.image.save(screen, DIRPATH+'/query1.png')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
