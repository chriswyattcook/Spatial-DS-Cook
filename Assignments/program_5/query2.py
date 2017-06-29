from mongo_helper_class import *
from pygame_helper import *
import pprint as pp
import sys
import pygame


DIRPATH = os.path.dirname(os.path.realpath(__file__))

#display
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)

#separates argv
feature = sys.argv[1]
field = sys.argv[2]
field_value = float(sys.argv[3])
min_max = sys.argv[4]
max_results = int(sys.argv[5])
radius = float(sys.argv[6])

#run db query for next airport within the r
#find all vol as red, eq as blue, meteor as green
#repeat steps until at end_pt
mh = mongoHelper()

#get coords of feature
feature_info =  mh.get_doc_by_keyword()
feature_coords = mh.get_coordinates(feature_info)

coords = []
coords.append(feature_coords)

# Create dictionary to send to adjust method
extremes = {}
extremes['max_x'] = feature_info[0]
extremes['min_x'] = feature_info[0]
extremes['max_y'] = feature_info[1]
extremes['min_y'] = feature_info[1]
 
adj = adjust_location_coords(extremes,coords,width,height)

print(coords)
sys.exit()


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
        
