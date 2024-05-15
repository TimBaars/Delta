import cv2
import numpy as np
import math
import random

class Nodes:
    """Class to store the RRT graph"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent_x = []
        self.parent_y = []

class RRT:
    def __init__(self):
        self.node_list = []
        self.x_list = []
        self.y_list = []

    def collision(self, x1, y1, x2, y2):
        color = []
        x = list(np.arange(x1, x2, (x2 - x1) / 100))
        y = list(((y2 - y1) / (x2 - x1)) * (x - x1) + y1)
        for i in range(len(x)):
            color.append(self.img[int(y[i]), int(x[i])])
        if 0 in color:
            return True  # collision
        else:
            return False  # no collision

    def check_collision(self, x1, y1, x2, y2, stepSize):
        _, theta = self.dist_and_angle(x2, y2, x1, y1)
        x = x2 + stepSize * np.cos(theta)
        y = y2 + stepSize * np.sin(theta)

        hy, hx = self.img.shape
        if y < 0 or y > hy or x < 0 or x > hx:
            directCon = False
            nodeCon = False
        else:
            if self.collision(x, y, self.end[0], self.end[1]):
                directCon = False
            else:
                directCon = True

            if self.collision(x, y, x2, y2):
                nodeCon = False
            else:
                nodeCon = True

        return (x, y, directCon, nodeCon)

    def dist_and_angle(self, x1, y1, x2, y2):
        dist = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
        angle = math.atan2(y2 - y1, x2 - x1)
        return (dist, angle)

    def nearest_node(self, x, y):
        temp_dist = []
        for i in range(len(self.node_list)):
            dist, _ = self.dist_and_angle(x, y, self.node_list[i].x, self.node_list[i].y)
            temp_dist.append(dist)
        return temp_dist.index(min(temp_dist))

    def rnd_point(self, h, l):
        new_y = random.randint(0, h)
        new_x = random.randint(0, l)
        return (new_x, new_y)

    def RRT(self, img, img2, coordinates, stepSize):
        self.x_list = []
        self.y_list = []
        self.start = (coordinates[0], coordinates[1])
        self.end = (coordinates[2], coordinates[3])
        self.img = img
        self.img2 = img2
        h, l = self.img.shape

        self.node_list = [Nodes(self.start[0], self.start[1])]
        self.node_list[0].parent_x.append(self.start[0])
        self.node_list[0].parent_y.append(self.start[1])

        cv2.circle(self.img2, (self.start[0], self.start[1]), 5, (0, 0, 255), thickness=3, lineType=8)
        cv2.circle(self.img2, (self.end[0], self.end[1]), 5, (0, 0, 255), thickness=3, lineType=8)

        i = 1
        pathFound = False
        while pathFound == False:
            nx, ny = self.rnd_point(h, l)
            nearest_ind = self.nearest_node(nx, ny)
            nearest_x = self.node_list[nearest_ind].x
            nearest_y = self.node_list[nearest_ind].y
            tx, ty, directCon, nodeCon = self.check_collision(nx, ny, nearest_x, nearest_y, stepSize)

            if directCon and nodeCon:
                self.node_list.append(Nodes(tx, ty))
                #print(f"Path node: {tx}, {ty}")
                self.node_list[i].parent_x = self.node_list[nearest_ind].parent_x.copy()
                self.node_list[i].parent_y = self.node_list[nearest_ind].parent_y.copy()
                self.node_list[i].parent_x.append(tx)
                self.node_list[i].parent_y.append(ty)
                
                cv2.circle(self.img2, (int(tx), int(ty)), 2, (0, 0, 255), thickness=3, lineType=8)
                cv2.line(self.img2, (int(tx), int(ty)), (int(self.node_list[nearest_ind].x), int(self.node_list[nearest_ind].y)), (0, 255, 0), thickness=1, lineType=8)
                cv2.line(self.img2, (int(tx), int(ty)), (self.end[0], self.end[1]), (255, 0, 0), thickness=2, lineType=8)

                for j in range(len(self.node_list[i].parent_x) - 1):
                    self.x_list.append(self.node_list[i].parent_x[j+1])
                    self.y_list.append(self.node_list[i].parent_y[j+1])
                    #print(f"Parent node: {self.node_list[i].parent_x[j]}, {self.node_list[i].parent_y[j]}")
                    cv2.line(self.img2, (int(self.node_list[i].parent_x[j]), int(self.node_list[i].parent_y[j])), (int(self.node_list[i].parent_x[j + 1]), int(self.node_list[i].parent_y[j + 1])), (255, 0, 0), thickness=2, lineType=8)

                #cv2.imwrite("Pathplanning/media/" + str(i) + ".jpg", self.img2)
                cv2.imwrite("Pathplanning/out.jpg", self.img2)

                return self.node_list, self.x_list, self.y_list

            elif nodeCon:
                self.node_list.append(Nodes(tx, ty))
                #print(f"Path node: {tx}, {ty}")
                self.node_list[i].parent_x = self.node_list[nearest_ind].parent_x.copy()
                self.node_list[i].parent_y = self.node_list[nearest_ind].parent_y.copy()
                self.node_list[i].parent_x.append(tx)
                self.node_list[i].parent_y.append(ty)
                i += 1

                cv2.circle(self.img2, (int(tx), int(ty)), 2, (0, 0, 255), thickness=3, lineType=8)
                cv2.line(self.img2, (int(tx), int(ty)), (int(self.node_list[nearest_ind].x), int(self.node_list[nearest_ind].y)), (0, 255, 0), thickness=1, lineType=8)
                cv2.imwrite("Pathplanning/media/" + str(i) + ".jpg", self.img2)
                continue

            else:
                continue
