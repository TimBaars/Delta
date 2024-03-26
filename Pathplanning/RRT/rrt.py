"""

Path planning with Rapidly-Exploring Random Trees (RRT)

author: Aakash(@nimrobotics)
web: nimrobotics.github.io

"""

import cv2
import numpy as np
import math
import random
import os
import time

class Nodes:
    """Class to store the RRT graph"""
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.parent_x = []
        self.parent_y = []

class RRT:
    def __init__(self):
        self.node_list = [0]
        
    def collision(self, x1,y1,x2,y2):
        color=[]
        x = list(np.arange(x1,x2,(x2-x1)/100))
        y = list(((y2-y1)/(x2-x1))*(x-x1) + y1)
        #print("collision",x,y)
        for i in range(len(x)):
            #print(int(x[i]),int(y[i]))
            color.append(self.img[int(y[i]),int(x[i])])
        if (0 in color):
            return True #collision
        else:
            return False #no-collision

    # check the  collision with obstacle and trim
    def check_collision(self, x1,y1,x2,y2, stepSize):
        _,theta = self.dist_and_angle(x2,y2,x1,y1)
        x=x2 + stepSize*np.cos(theta)
        y=y2 + stepSize*np.sin(theta)
        #print(x2,y2,x1,y1)
        #print("theta",theta)
        #print("check_collision",x,y)

        # TODO: trim the branch if its going out of image area
        # print("Image shape",self.img.shape)
        hy,hx=self.img.shape
        if y<0 or y>hy or x<0 or x>hx:
            #print("Point out of image bound")
            directCon = False
            nodeCon = False
        else:
            # check direct connection
            if self.collision(x,y,self.end[0],self.end[1]):
                directCon = False
            else:
                directCon=True

            # check connection between two nodes
            if self.collision(x,y,x2,y2):
                nodeCon = False
            else:
                nodeCon = True

        return(x,y,directCon,nodeCon)

    # return dist and angle b/w new point and nearest node
    def dist_and_angle(self, x1,y1,x2,y2):
        dist = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
        angle = math.atan2(y2-y1, x2-x1)
        return(dist,angle)

    # return the neaerst node index
    def nearest_node(self, x,y):
        temp_dist=[]
        for i in range(len(self.node_list)):
            dist,_ = self.dist_and_angle(x,y,self.node_list[i].x,self.node_list[i].y)
            temp_dist.append(dist)
        return temp_dist.index(min(temp_dist))

    # generate a random point in the image space
    def rnd_point(self, h,l):
        new_y = random.randint(0, h)
        new_x = random.randint(0, l)
        return (new_x,new_y)


    def RRT(self, img, img2, coordinates, stepSize):
        self.start =(coordinates[0],coordinates[1])
        self.end =(coordinates[2],coordinates[3])
        self.img = img
        self.img2 = img2
        h,l= self.img.shape # dim of the loaded image
        # print(self.img.shape) # (384, 683)
        # print(h,l)


        # insert the starting point in the node class
        # self.node_list = [0] # list to store all the node points         
        self.node_list[0] = Nodes(self.start[0],self.start[1])
        self.node_list[0].parent_x.append(self.start[0])
        self.node_list[0].parent_y.append(self.start[1])

        # display start and end
        cv2.circle(self.img2, (self.start[0],self.start[1]), 5,(0,0,255),thickness=3, lineType=8)
        cv2.circle(self.img2, (self.end[0],self.end[1]), 5,(0,0,255),thickness=3, lineType=8)

        i=1
        pathFound = False
        while pathFound==False:
            nx,ny = self.rnd_point(h,l)
            #print("Random points:",nx,ny)

            nearest_ind = self.nearest_node(nx,ny)
            nearest_x = self.node_list[nearest_ind].x
            nearest_y = self.node_list[nearest_ind].y
            #print("Nearest node coordinates:",nearest_x,nearest_y)

            #check direct connection
            tx,ty,directCon,nodeCon = self.check_collision(nx,ny,nearest_x,nearest_y, stepSize)
            #print("Check collision:",tx,ty,directCon,nodeCon)

            if directCon and nodeCon:
                #print("Node can connect directly with end")
                self.node_list.append(i)
                self.node_list[i] = Nodes(tx,ty)
                self.node_list[i].parent_x = self.node_list[nearest_ind].parent_x.copy()
                self.node_list[i].parent_y = self.node_list[nearest_ind].parent_y.copy()
                self.node_list[i].parent_x.append(tx)
                self.node_list[i].parent_y.append(ty)

                cv2.circle(self.img2, (int(tx),int(ty)), 2,(0,0,255),thickness=3, lineType=8)
                cv2.line(self.img2, (int(tx),int(ty)), (int(self.node_list[nearest_ind].x),int(self.node_list[nearest_ind].y)), (0,255,0), thickness=1, lineType=8)
                cv2.line(self.img2, (int(tx),int(ty)), (self.end[0],self.end[1]), (255,0,0), thickness=2, lineType=8)

                #print("Path has been found")
                #print("parent_x",self.node_list[i].parent_x)
                for j in range(len(self.node_list[i].parent_x)-1):
                    cv2.line(self.img2, (int(self.node_list[i].parent_x[j]),int(self.node_list[i].parent_y[j])), (int(self.node_list[i].parent_x[j+1]),int(self.node_list[i].parent_y[j+1])), (255,0,0), thickness=2, lineType=8)
                # cv2.waitKey(1)
                cv2.imwrite("Pathplanning/media/"+str(i)+".jpg",self.img2)
                cv2.imwrite("Pathplanning/out.jpg",self.img2)
                return self.node_list

            elif nodeCon:
                #print("Nodes connected")
                self.node_list.append(i)
                self.node_list[i] = Nodes(tx,ty)
                self.node_list[i].parent_x = self.node_list[nearest_ind].parent_x.copy()
                self.node_list[i].parent_y = self.node_list[nearest_ind].parent_y.copy()
                # print(i)
                # print(self.node_list[nearest_ind].parent_y)
                self.node_list[i].parent_x.append(tx)
                self.node_list[i].parent_y.append(ty)
                i=i+1
                # display
                cv2.circle(self.img2, (int(tx),int(ty)), 2,(0,0,255),thickness=3, lineType=8)
                cv2.line(self.img2, (int(tx),int(ty)), (int(self.node_list[nearest_ind].x),int(self.node_list[nearest_ind].y)), (0,255,0), thickness=1, lineType=8)
                cv2.imwrite("Pathplanning/media/"+str(i)+".jpg",self.img2)
                continue

            else:
                #print("No direct con. and no node con. :( Generating new rnd numbers")
                continue

