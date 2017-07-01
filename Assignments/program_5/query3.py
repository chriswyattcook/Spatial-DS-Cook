from mongo_features_helper import *
from mapping_helper import *
from dbscan import *
import pprint as pp
import pygame
import sys,os

DIRPATH = os.path.dirname(os.path.realpath(__file__))

#display
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)
color_list = {'volcanos':(255,0,0),'earthquakes':(70,173,212),'meteorites':(76,187,23)}
box_color = (255,255,0)

#run db query for next airport within the r
#find all vol as red, eq as blue, meteor as green
#repeat steps until at end_pt

pygame.init()
bg = pygame.image.load(DIRPATH+'/world_map.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('query3')
screen.fill(background_colour)
pygame.display.flip()

#separate sys.argv
feature = sys.argv[1]
min_pts = float(sys.argv[2])
eps = float(sys.argv[3])

mh = mongoHelper()

res = []
points = []
extremes = {}
result_list = mh.client['world_data'][feature].find()

extremes, points = find_extremes(result_list, width, height)

points = adjust_location_coords(extremes,points,width,height)

mbrs = calculate_mbrs(points, eps, min_pts)

screen.blit(bg, (0, 0))
pygame.display.flip()

running = True
while running:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      
    for mbr in mbrs:
         pygame.draw.polygon(screen, box_color, mbr, 2)
         pygame.display.flip()
    for pt in points:
        pygame.draw.circle(screen, color_list[feature], pt, 2,1)
        pygame.display.flip()
    pygame.image.save(screen, DIRPATH+'/query3.png')

    