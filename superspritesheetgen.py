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
e = 1

for filename in filenames:
    if e == 1:
        print ("Working...")
        e = 0
    img = Image.open(filename)
    img = img.resize((fsizex,fsizey))
    xoffset = xmod * fsizex
    yoffset = ymod * fsizey
    imgfinal.paste(img, ((xoffset),(yoffset)))
    loop = loop + 1
    #print (loop)
    if xmod == int((gsize - 1)):
        ymod = ymod + 1
    xmod = int(loop % gsize)

imgfinal.resize((tsizex,tsize))
print ("Done!")
#imgfinal.show()

save = easygui.indexbox(msg='Where would you like to save your spritesheet?', title='', choices=('User Defined', 'Parent Folder(default)', 'Same Folder(not recommended)'), image=None)

if save == 0:
    savepath = easygui.filesavebox()
    if (savepath[-4:]) != (filetype[-4:]):
        savepath = savepath + (filetype[-4:])
    imgfinal.save(savepath, "png")
if save == 1:
    imgfinal.save("../sss_result.png", "png")
if save == 2:
    imgfinal.save("sss_result.png", "png")

exit
