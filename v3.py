import numpy as np
import cv2
from Color import Color
from random import randint, choice
import os

deltas = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def fill(x,y,c,img):
    if inBounds(img.shape, x, y):
        img[y,x] = c.bgr()
        return True
    else:
        return False

def inBounds(shape, x, y):
    maxY, maxX, _ = shape
    return x >= 0 and y>= 0 \
            and x<maxX \
            and y<maxY

def isSurrounded(x,y,unused):
    for dX, dY in deltas:
        #print("Checking ({},{}): {}".format(x+dX, y+dY,(x+dX, y+dY) in unused))
        if (x+dX, y+dY) in unused:
            return False
    return True



def delta():
    dX = 1-2*randint(0,1)
    dY = 1-2*randint(0,1)
    return dX, dY

def tele(maxX, maxY):
    return randint(0,maxX), randint(0,maxY)


if __name__ == "__main__":
    #               y,  x, c
    maxX, maxY = 1920, 1080
    img = np.zeros((maxY, maxX, 3), dtype=np.uint8)
    c = Color(255, 255, 255)

    x, y = randint(0,maxX), randint(0,maxY)
    denom = 100 / (maxX * maxY)

    pixelsWritten = 0
    while c.bgr().any() > 0 and pixelsWritten < maxX*maxY:
        #print("({}+{},{}+{})".format(x,1,y,1))
        if (x+1<maxX and img[y,x+1].any() != 0 or not x+1<maxX) \
                and (x-1>=0 and img[y, x-1].any() != 0 or not x-1>=0) \
                and (y+1<maxY and img[y+1,x].any() != 0 or not y+1<maxY) \
                and (y-1>=0 and img[y-1,x].any() != 0 or not y-1>=0):
            # teleport to a new location
            #x, y = choice([(a,b) for a in range(maxX) for b in range(maxY) if img[b,a].all() == 0])
            # new teleport
            radR = 1
            pointFound = False
            while x is not None and y is not None and not pointFound:
                if x+radR>=maxX and y+radR >= maxY and x-radR<0 and y-radR<0:
                    x,y = None, None
                    break
                if y + radR < maxY and not pointFound:
                    for offX in range(-radR, radR + 1):
                        if offX + x >= 0 and offX + x < maxX:
                            #print("{}: ({},{})".format(radR, x + offX, y + radR))
                            if img[y+radR,x+offX].all() == 0:
                                x,y = x+offX,y+radR
                                pointFound = True
                                break
                if x + radR < maxX and not pointFound:
                    for offY in range(-radR + 1, radR + 1):
                        if y - offY >= 0 and y - offY < maxY:
                            #print("{}: ({},{})".format(radR, x + radR, y - offY))
                            if img[y-offY,x+radR].all() == 0:
                                x,y = x+radR,y-offY
                                pointFound = True
                                break
                if y - radR >= 0 and not pointFound:
                    for offX in range(-radR + 1, radR + 1):
                        if x - offX >= 0 and x - offX < maxX:
                            #print("{}: ({},{})".format(radR, x - offX, y - radR))
                            if img[y-radR,x-offX].all() == 0:
                                x,y = x-offX,y-radR
                                pointFound = True
                                break
                if x - radR >= 0 and not pointFound:
                    for offY in range(-radR + 1, radR):
                        if y - offY >= 0 and y - offY < maxY:
                            #print("{}: ({},{})".format(radR, x - radR, y - offY))
                            if img[y-offY,x-radR].all() == 0:
                                x,y = x-radR,y-offY
                                pointFound = True
                                break
                radR += 1
        else:
            # pick a neighbor if it isn't colored in yet
            points = [(x + dX, y + dY) for dX, dY in deltas if inBounds(img.shape, x+dX, y+dY) and img[y+dY,x+dX].all() == 0]
            try:
                x,y = choice(points)
            except IndexError:
                if y-1 >= 0:
                    print("             {}".format(img[y-1,x]))

                if x-1 >= 0:
                    print("{}\t".format(img[y,x-1]),end="")
                else:
                    print("             ",end="")
                print("{}".format(img[y,x]),end="")
                if x+1 < maxX:
                    print(" {}".format(img[y,x+1]))
                else:
                    print()


                if y+1<maxY:
                    print("             {}".format(img[y+1,x]))
                quit()

        if x is None and y is None:
            break


        fill(x,y,c,img)
        pixelsWritten += 1
        c.dec(pixelsWritten, maxX*maxY)
        #print(c.bgr(), end="\r")


    cv2.imshow("Image", img)

    try:
        os.remove("out.png")
        print("'out.png' was removed")
    except FileNotFoundError:
        print("'out.png' doesn't exist.  Can't delete non-existant file.")

    cv2.imwrite("out.png",img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()