from PIL import Image

import easygui
import math
import glob
import os
import time
import Tkinter

print ("User Input Dialog Opened")
opath = easygui.fileopenbox(title='Pick the first image in an image sequence!')
test = Image.open(opath)
imgw = float(test.width)
imgh = float(test.height)
h2wratio = float(imgw/imgh)
print ("Width to Height Ratio: ", h2wratio)

if h2wratio != 1:
    print ("User Input Dialog Opened")
    fixaspect = easygui.indexbox(msg='Your image is not square.', title='', choices=('Maintain(Rectangular Output)', 'Approximate(Square Output)'), image=None)
    fix = 1

opathdir = os.path.dirname(opath)
os.chdir(opathdir)

print ("User Input Dialog Opened")
tsize = easygui.integerbox(msg='Texture Size (Height)?', lowerbound=4, upperbound=33333)
if fixaspect == 0:
    tsizex = int(tsize * h2wratio)
if fixaspect == 1:
    tsizex = tsize

filetype = ("*" + opath[-4:])

filenames = glob.glob(filetype)
filenames.sort()

if fixaspect == 0:
    gsize = int(math.ceil(math.sqrt(len(filenames))))
    gsizey = gsize
if fixaspect == 1:
    gsize = int(math.ceil(math.sqrt(len(filenames))))
    gsizesq = gsize * gsize
    if h2wratio > 1:
        while fix == 1:
            gsizey = gsize
            gsizex = int(gsize/h2wratio)
            gtotal = gsizex * gsizey
            while gtotal < gsizesq:
                if gsizey > (gsizex*h2wratio):
                    gsizex = gsizex + 1
                else:
                    gsizey = gsizey + 1
                gtotal = gsizey * gsizex
            if (gtotal - len(filenames)) > gsizey:
                gsizex = gsizex - 1
            fix = 0
    if h2wratio < 1:
        while fix == 1:
            gsizex = gsize
            gsizey = int(gsize*h2wratio)
            gtotal = gsizex * gsizey
            while gtotal < gsizesq:
                if gsizex > (gsizey/h2wratio):
                    gsizey = gsizey + 1
                else:
                    gsizex = gsizex + 1
                gtotal = gsizex * gsizey
            if (gtotal - len(filenames)) > gsizex:
                gsizey = gsizey - 1
            fix = 0

fsizex = tsize/gsizex
fsizey = tsize/gsizey
xtsizex = int(gsizex * fsizex)
xtsizey = int(gsizey * fsizey)

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
    if xmod == int((gsizex - 1)):
        ymod = ymod + 1
    xmod = int(loop % gsizex)

imgfinal = imgfinal.resize((tsizex,tsize), resample=3)
print ("SpriteSheet Assembled")

print(tsizex,tsize)
print ("User Input Dialog Opened")
save = easygui.indexbox(msg='Where would you like to save your spritesheet?', title='', choices=('User Defined', 'Parent Folder(default)', 'Same Folder(not recommended)'), image=None)

if save == 0:
    savepath = easygui.filesavebox()
    if (savepath[-4:]) != (filetype[-4:]):
        savepath = savepath + (filetype[-4:])
    print ("Saving SpriteSheet...")
    imgfinal.save(savepath, "png")
if save == 1:
    print ("Saving SpriteSheet...")
    imgfinal.save("../sss_result.png", "png")
if save == 2:
    print ("Saving SpriteSheet...")
    imgfinal.save("sss_result.png", "png")

print ("All done.")

exit
