import os
import os.path
import math
import Queue
from collections import deque
from PIL import Image

# from __future__ import print_function

delta = [[1, 0], [0, 1], [-1, 0], [0, -1]]


def imageCleaner(imageFile):

    print "processing %s ......" % (imageFile)

    file, ext = os.path.splitext(imageFile)
    file = file +  ".PNG"

    _,filename =  os.path.split(imageFile)

    try:
        im = Image.open(imageFile)
    except IOError:
        print "%s is not picture" % (filename)
    else:
        
        if im.mode == "RGB":
            print "%s picture Mode is :%s,convert to RGBA" % (filename,im.mode)
            im = im.convert("RGBA")
        else:
            if im.mode != "RGBA":
                print "%s is wrong picture Mode Mode:%s" % (filename,im.mode)
                return
        
        px = im.load()

        width, height = im.size

        queue = deque()

        queue.append((0, 0))
        queue.append((width - 1, 0))
        queue.append((width - 1, height - 1))
        queue.append((0, height - 1))

        px[0, 0] = (0, 0, 0, 0)
        px[width - 1, 0] = (0, 0, 0, 0)
        px[width - 1, height - 1] = (0, 0, 0, 0)
        px[0, height - 1] = (0, 0, 0, 0)

        while len(queue) != 0:

            point = queue.popleft()
            a = point[0]
            b = point[1]


            for index in range(4):

                x = a + delta[index][0]
                y = b + delta[index][1]

                if x > (width - 1) or x < 0 or y > (height - 1) or y < 0:
                    continue
                curPex = px[x, y]
                if isWhite(curPex) == True:
                    px[x, y] = (0, 0, 0, 0)
                    queue.append((x, y))

        im.save(file, "PNG")
        im.close()

    return


def isWhite(px):
    r = px[0]
    g = px[1]
    b = px[2]
    value = max(abs(r - 255), abs(g - 255), abs(b - 255)) < 10

    return value


print "image cleaner  Begin"
curpath = os.path.abspath('.')
foldPath = curpath + "/" + "images"
for root, dirs, files in os.walk(foldPath):
    for name in files:
        imageFile = os.path.join(root, name)
        imageCleaner(imageFile)


print "image cleaner  finish"

