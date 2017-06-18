# Chris Cook
# 4553 Spatial Data Structures
# Program 2 Part 1
# Due: June 20, 2017

import pygame
import random
from dbscan import *
import sys,os
import pprint as pp
from read_crime_data import *


def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    # for id,cpoints in clusters.items():
    #     xs = []
    #     ys = []
    #     for p in cpoints:
    #         xs.append(p[0])
    #         ys.append(p[1])
    #     max_x = max(xs) 
    #     max_y = max(ys)
    #     min_x = min(xs)
    #     min_y = min(ys)
    #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    # return mbrs

    """
    Using list index value to iterate over the clusters dictionary
    Does same as above
    """
    for id in range(len(clusters)-1):
        xs = []
        ys = []
        for p in clusters[id]:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs


def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1000, 1000)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('NYPD Crime')
screen.fill(background_colour)

pygame.display.flip()

epsilon = 1
min_pts = 20

points = []

crimes=[]

crime_data = {}

files=["bronx","brooklyn","manhattan","queens","staten_island"]
colors = [(2,120,120),(128,22,56),(194,35,38),(243,115,56),(253,182,50)]

for i in range(len(files)):
    crimes += (read_crime_data(files[i]))
    crime_data[files[i]] = len(crimes),colors[i]

#print(crime_data)
xs = []
ys = []

for i in range(len(crimes)):
    if(crimes[i][19]== ''):
        continue
    else:    
        x = int(crimes[i][19])/1000
        xs.append(int(crimes[i][19])/1000)
    if(crimes[i][20]== ''):
        continue
    else:    
        y = int(crimes[i][20])/1000
        ys.append(int(crimes[i][20])/1000)
    #print(x,y)
    points.append((x,y))

MaxX= 1067.226
MaxY= 271.820
MinX= 913.357
MinY= 121.250

scaled_pts = []

for z in range(len(points)):
    new_x = round((points[z][0]-MinX)/((MaxX-MinX))*width)
    new_y = round((points[z][1]-MinY)/((MaxY-MinY))*height)
    scaled_pts.append((new_x,new_y))
   # print(new_x,new_y)
    

#mbrs = calculate_mbrs(scaled_pts, epsilon, min_pts)

running = True
while running:
    for i in range(len(scaled_pts)):
        if i < crime_data[files[0]][0]:
            pygame.draw.circle(screen,colors[0],scaled_pts[i],1,0)
        if i > crime_data[files[0]][0] and i < crime_data[files[1]][0]:
            pygame.draw.circle(screen,colors[1],scaled_pts[i],1,0)
        if i > crime_data[files[1]][0] and i < crime_data[files[2]][0]:
            pygame.draw.circle(screen,colors[2],scaled_pts[i],1,0)
        if i > crime_data[files[2]][0] and i < crime_data[files[3]][0]:
            pygame.draw.circle(screen,colors[3],scaled_pts[i],1,0)
        if i > crime_data[files[3]][0] and i < crime_data[files[4]][0]:
            pygame.draw.circle(screen,colors[4],scaled_pts[i],1,0)
    #for p in scaled_pts:
        #pygame.draw.circle(screen, black, p, 1, 0)
   # for mbr in mbrs:
       #pygame.draw.polygon(screen, black, mbr, 2)
    pygame.image.save(screen , DIRPATH+'/all_buroughs_screen_shot.png')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clean_area(screen,(0,0),width,height,(255,255,255))
            scaled_pts.append(event.pos)
           # mbrs = calculate_mbrs(scaled_pts, epsilon, min_pts)
    pygame.display.flip()
