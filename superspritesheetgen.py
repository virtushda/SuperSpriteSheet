from PIL import Image

import easygui
import math
import glob
import os
import time

opath = easygui.fileopenbox(title='Pick the first image in an image sequence!')
opathdir = os.path.dirname(opath)
print opathdir
os.chdir(opathdir)
tsize = easygui.integerbox(msg='Texture Size?', lowerbound=16, upperbound=8192)

filetype = ("*" + opath[-4:])
print (filetype)

imgfinal = Image.new("RGB", (tsize, tsize))

filenames = glob.glob(filetype)
filenames.sort()
gsize = int(math.ceil(math.sqrt(len(filenames))))
print (gsize)
fsize = int(tsize/gsize)
print (fsize)

loop = 0
xmod = 0
ymod = 0

for filename in filenames:
    img = Image.open(filename)
    print (filename)
    imgcopy = img.copy()
    imgcopy = imgcopy.resize((fsize,fsize))
    xoffset = xmod * fsize
    yoffset = ymod * fsize
    imgfinal.paste(imgcopy, ((xoffset),(yoffset)))
    #print ("I am actually working this time.")
    loop = loop + 1
    if xmod == int((gsize - 1)):
        ymod = ymod + 1
    xmod = int(loop % gsize)

imgfinal.show()
