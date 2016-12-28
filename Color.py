import numpy as np
from random import randint
class Color:
    def __init__(self, r, g, b):
        self.red = r
        self.blue = b
        self.green = g

        self.i = 255
        self.j = 255
        self.k = 255

    def rgb(self):
        v = np.zeros(3, dtype=np.uint8)
        v[0] = self.red
        v[1] = self.green
        v[2] = self.blue
        return v

    def bgr(self):
        v = np.zeros(3, dtype=np.uint8)
        v[0] = self.blue
        v[1] = self.green
        v[2] = self.red
        return v

    '''def dec(self, amnt):
        down = 3*5
        up   = 3*1
        x = randint(1,9)
        if x in [i for i in range(1,int(up/3)+1)]:
            self.red = min(self.red + amnt, 255)
        elif x in [i for i in range(int(up/3+1),int(2*up/3)+1)]:
            self.green = min(self.green + amnt, 255)
        elif x == [i for i in range(int(2*up/3+1),int(3*up/3)+1)]:
            self.blue = min(self.blue + amnt, 255)
        elif x in [i for i in range(up+1, int(up+down/3)+1)]:#self.red > 0:
            self.red = max(self.red - amnt, 0)
        elif x in [i for i in range(int(up+down/3)+1,int(up+2*down/3)+1)]:#self.green > 0:
            self.green = max(self.green - amnt, 0)
        elif x in [i for i in range(int(up+2*down/3)+1,int(up+3*down/3)+1)]:#self.blue > 0:
            self.blue = max(self.blue - amnt, 0)
    '''

    def dec(self, amnt, of):
        decamnt = randint(2,3)
        self.k -= decamnt
        if self.k < 0:
            self.j -= decamnt
            self.k = 255
            #print("k rolled over. j={}, i={}".format(self.j, self.i))
        if self.j < 0:
            self.i -= decamnt
            self.j = 255
            print("j rolled over. i={}.  pixel {}/{}".format(self.i, amnt, of))
        if self.i < 0:
            self.i = 0
            self.j = 0
            self.k = 0
        self.red = self.i
        self.green = self.j
        self.blue = self.k