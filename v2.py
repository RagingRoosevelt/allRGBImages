import cv2
import numpy as np
from random import randint, shuffle
from math import ceil

class Color:
    def __init__(self, r, g, b):
        self.red = r
        self.blue = b
        self.green = g

    def rgb(self):
        v = np.zeros(3)
        v[0] = self.red
        v[1] = self.green
        v[2] = self.blue
        return v

    def __add__(self, other):
        if isinstance(other, int):
            if self.red < 255:
                return Color(min(self.red+other,255), self.green, self.blue)
            elif self.green < 255:
                return Color(self.red, min(self.green+other,255), self.blue)
            elif self.blue < 255:
                return Color(self.red, self.green, min(self.blue+other,255))
            else:
                return Color(255,255,255)
    def __sub__(self, other):
        if isinstance(other, int):
            if self.red > 0:
                return Color(max(self.red-other,0), self.green, self.blue)
            elif self.green > 0:
                return Color(self.red, max(self.green-other,0), self.blue)
            elif self.blue > 0:
                return Color(self.red, self.green, max(self.blue-other,0))
            else:
                return Color(0,0,0)


class Img:
    def __init__(self, h, w, scale):
        self.scale = scale
        self.height = h*(2*self.scale + 1)
        self.width = w*(2*self.scale + 1)
        self.img = np.zeros((self.height, self.width, 3), np.uint8)
        self.filled = np.zeros((self.height, self.width, 1), np.bool)

        x = (2*self.scale+1)*randint(0, h-1)+self.scale
        y = (2*self.scale+1)*randint(0, w-1)+self.scale
        self.c = Color(255,255,255)

        self.fillImage(x, y)
        #openNeighbors = self.openNeighbors(x,y)

    def fillImage(self, x, y):
        print("working on point ({},{})".format(x,y))
        if not self.filled[x,y] and self.c.rgb().any() >= 0:
            self.fill(x,y,self.c)

            deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            deltas = [(dX*(2*self.scale+1), dY*(2*self.scale+1)) for dX,dY in deltas]
            print(deltas)
            shuffle(deltas)
            for dX, dY in deltas:
                if 0 <= (x + dX) and (x + dX) < self.width and \
                        0 <= (y + dY) and (y + dY) < self.height:
                    self.fillImage(x+dX, y+dY)

    def fill(self, x, y, c):
        deltas = [(i,j) for i in range(-self.scale, self.scale+1) for j in range(-self.scale, self.scale+1)]

        if not self.filled[x,y]:

            for dX, dY in deltas:
                if 0 <= (x + dX) and (x + dX) < self.width and \
                        0 <= (y + dY) and (y + dY) < self.height:
                    if not self.filled[x+dX,y+dY]:
                        self.filled[x+dX,y+dY] = True
                        self.img[x+dX,y+dY] = c.rgb()

            self.c -= 1

    def openNeighbors(self, x, y):
        openNeighbors = []

        deltas = [(-1,0), (1,0), (0,-1), (0,1)]

        for dX, dY in deltas:
            if (x+dX) >= 0 and (x+dX) < self.w and \
                    (y+dY) > 0 and (y+dY) < self.h and \
                    not self.filled[x+dX][y+dY]:
                openNeighbors.append((x+dX, y+dY))




i = Img(4072, 4072, 1)

cv2.imshow("", i.img)
cv2.waitKey(0)
cv2.destroyAllWindows()