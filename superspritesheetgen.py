from PIL import Image

import easygui
import math
import glob
import os
import time

opath = easygui.fileopenbox(title='Pick the first image in an image sequence!')
test = Image.open(opath)
imgw = float(test.width)
print (imgw)
imgh = float(test.height)
print (imgh)
h2wratio = float(imgw/imgh)
print (h2wratio)

opathdir = os.path.dirname(opath)
print opathdir
os.chdir(opathdir)

tsize = easygui.integerbox(msg='Texture Size (Height)?', lowerbound=4, upperbound=99999)
tsizex = int(tsize * h2wratio)

filetype = ("*" + opath[-4:])
print (filetype)

<<<<<<< HEAD
imgfinal = Image.new("RGB", (tsize, tsize))

=======
>>>>>>> origin/master
filenames = glob.glob(filetype)
filenames.sort()

gsize = int(math.ceil(math.sqrt(len(filenames))))
print (gsize)
fsizex = int(h2wratio * (tsize/gsize))
fsizey = int(tsize/gsize)
xtsizex = gsize * fsizex
print (xtsizex)
xtsizey = gsize * fsizey
print (xtsizey)

alpha = 0
if test.mode == "RGBA": 
    imgfinal = Image.new("RGBA", (xtsizex, xtsizey), (0,0,0,0))
    imgfinal.putalpha(0)
    alpha = 1
else:
    imgfinal = Image.new("RGB", (xtsizex, xtsizey))
    alpha = 0

loop = 0
xmod = 0
ymod = 0

for filename in filenames:
    img = Image.open(filename)
    imgcopy = img.copy()
<<<<<<< HEAD
    imgcopy = imgcopy.resize((fsize,fsize))
    xoffset = xmod * fsize
    yoffset = ymod * fsize
=======
    imgcopy = imgcopy.resize((fsizex,fsizey))
    xoffset = xmod * fsizex
    yoffset = ymod * fsizey
>>>>>>> origin/master
    imgfinal.paste(imgcopy, ((xoffset),(yoffset)))
    loop = loop + 1
    if xmod == int((gsize - 1)):
        ymod = ymod + 1
    xmod = int(loop % gsize)

imgfinal.resize((tsizex,tsize))
imgfinal.show()
<<<<<<< HEAD
=======
imgfinal.save("../ssresult.png", "png")

exit
>>>>>>> origin/master
