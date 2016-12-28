from random import randint
from PIL import Image
import numpy as np

class Img:
    def __init__(self, w, h):
        self.filled  = matGen(False, h, w)
        self.colors = arrGen(0, h, w).astype('uint8')
        self.w = w
        self.h = h
        
    def openNeighbors(self, x,y):
        openNeighbors = []

        deltas = [(-1,0), (1,0), (0,-1), (0,1)]

        for dX, dY in deltas:
            if (x+dX) >= 0 and (x+dX) < self.w and \
                    (y+dY) > 0 and (y+dY) < self.h and \
                    not self.filled[x+dX][y+dY]:
                openNeighbors.append((x+dX, y+dY))
            
        return openNeighbors
        
    def fillPoint(self, x, y, color):
        if self.filled[x][y]:
            return False
            
        self.colors[x][y] = color
        self.filled[x][y] = True
        
        return True
        
    def print(self):
        print(self.colors)
        '''
        for row in self.colors:
            print("".join("{:03d} ".format(x) for x in row))
        '''
        
    def image(self):
        self.i = Image.new("RGB", (self.w, self.h))
        #t = [(x,x,x) for x in self.colors]
        #print(t)
        self.i.fromarray(self.color)
        return self.i
       
        
def arrGen(fill, w, h):
    return np.array(matGen(fill, w, h))
def matGen(fill, w, h):
    return [[fill for x in range(w)] for y in range(h)]
    
    
if __name__ == "__main__":
    x = randint(0,15)
    y = randint(0,15)
    color = 255
    img = Img(16,16)

    while color >= 0:
        openNeighbors = img.openNeighbors(x,y)
        
        if len(openNeighbors) == 0:
            break
        else:
            (x, y) = openNeighbors[randint(0,len(openNeighbors)-1)]
            
            #print("Filling ({}, {})".format(x,y))
            
            img.fillPoint(x, y, color)
            color -= 1
            
    img.print()
    img.image()
    