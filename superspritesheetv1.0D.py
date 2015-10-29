#Seth Kelley 2015
from PIL import Image

import easygui
import math
import glob
import os
import sys
import time
import Tkinter

restart = 1

while restart == 1:
    print ("Welcome!")
    print ("User Input Dialog Opened")
    looper = 1
    while looper == 1:
        opath = easygui.fileopenbox(title='Pick the first image in an image sequence!')
        if opath != '.':
            looper = 0
            
    #build information about the image to work with
    test = Image.open(opath)
    imgw = float(test.width)
    imgh = float(test.height)
    imgs = str(test.size)
    oframes = int(imgw * imgh)
    h2wratio = float(imgw/imgh)
    print ("Imported Frame Width, Height: %s" %imgs)
    print ("Width to Height Ratio: %f" %h2wratio)

    #Maintain: Create final image based on frame's original aspect ratio
    #Approximate: Adjust x&y grid sizes automagically to best fit frames into square
    if h2wratio != 1:
        fixaspect = None
        while fixaspect == None:
            print ("User Input Dialog Opened")
            fixaspect = easygui.indexbox(msg='Your image is not square.', title='', choices=('Maintain(Rectangular Output)', 'Approximate(Square Output)'), image=None)
    else:
        fixaspect = 0

    #change system directory
    opathdir = os.path.dirname(opath)
    os.chdir(opathdir)

    print ("User Input Dialog Opened")
    #Input desired image height and get width automatically
    tsize = None
    while tsize == None:
        tsize = easygui.integerbox(msg='Texture Size (Height)?', lowerbound=4, upperbound=33333)
    if fixaspect == 0:
        tsizex = int(tsize * h2wratio)
    if fixaspect == 1:
        tsizex = tsize

    filetype = ("*" + opath[-4:])
    #fetch files into list
    filenames = glob.glob(filetype)
    filenames.sort()

    gsizex = None
    gsizey = None

    def gridrecalc1( gsizex, gsizey ):
        gsize = int(math.ceil(math.sqrt(len(filenames))))
        gsizesq = gsize * gsize
        fix = 1
        while fix == 1:
            gsizey = gsize
            #Add bias that resembles image ratio
            gsizex = int(gsize/h2wratio)
            gtotal = gsizex * gsizey
            #Iterate grid size until it fits
            while gtotal < gsizesq:
                if gsizey > (gsizex*h2wratio):
                    gsizex = gsizex + 1
                else:
                    gsizey = gsizey + 1
                gtotal = gsizey * gsizex
            #Trim grid size if possible to save more detail
            if (gtotal - len(filenames)) >= gsizey:
                gsizex = gsizex - 1
            gtotal = gsizex * gsizey
            if (gtotal - len(filenames)) >= gsizex:
                gsizey = gsizey - 1
            fix = 0
            return gsizex, gsizey

    def gridrecalc2( gsizex, gsizey ):
        gsize = int(math.ceil(math.sqrt(len(filenames))))
        gsizesq = gsize * gsize
        fix = 1
        while fix == 1:
            gsizex = gsize
            #Add bias that resembles image ratio
            gsizey = int(gsize*h2wratio)
            gtotal = gsizex * gsizey
            #Iterate grid size until it fits
            while gtotal < gsizesq:
                if gsizex > (gsizey/h2wratio):
                    gsizey = gsizey + 1
                else:
                    gsizex = gsizex + 1
                gtotal = gsizex * gsizey
            #Trim grid size if possible to save more detail
            if (gtotal - len(filenames)) >= gsizex:
                gsizey = gsizey - 1
            gtotal = gsizex * gsizey
            if (gtotal - len(filenames)) >= gsizey:
                gsizex = gsizex - 1
            fix = 0
            return gsizex, gsizey

    #Recalculates grid size as necessary based on image dimensions
    if fixaspect == 0:
        gsize = int(math.ceil(math.sqrt(len(filenames))))
        gsizex = gsize
        gsizey = gsize
    if fixaspect == 1:
        if h2wratio > 1:
            gsizex, gsizey = gridrecalc1(gsizex,gsizey)
        if h2wratio < 1:
            gsizex, gsizey = gridrecalc2(gsizex,gsizey)
            

    print ("Grid Divisions X: %d" %gsizex)
    print ("Grid Divisions Y: %d" %gsizey)

    #framesize = full-texture-size / grid divisions
    fsizex = tsize/gsizex
    fsizey = tsize/gsizey
    #gets size of new frames after resize
    nframes = fsizex * fsizey
    xtsizex = int(gsizex * fsizex)
    xtsizey = int(gsizey * fsizey)

    #fetches percentage change between old and new frame sizes
    fsizech = float(float(nframes)/float(oframes))
    fsizech = (fsizech * 100)
    #Detail Change Info
    print ("Frame Size - New Relative to Imported: %f%%" %fsizech)
    #Low Detail Warning
    if fsizech < 25:
        print ("Warning! - Probable Loss of Detail")
    #Upscale Warning
    if fsizech > 100:
        print ("Warning! - You are upscaling each frame.")

    #Test for Alpha Channel and create new image from result
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
    prog = 0
    fprog = float(len(filenames))

    #fetch image, resize image, paste image loop
    for filename in filenames:
        if e == 1:
            print ("Compiling Sprites...")
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
        prog = int(100 * (float(loop)/fprog))
        progprint = int(loop % 12)
        if progprint == 1:
            print ("Progress: %d%%" %prog)
        if prog == 100:
            print ("Progress: 100%")

    #force final image to proper resolution(fixes rounding issues)
    imgfinal = imgfinal.resize((tsizex,tsize))
    print ("Sprite Sheet Assembled")

    print ("User Input Dialog Opened")
    save = None
    while save == None:
        save = easygui.indexbox(msg='Where would you like to save your spritesheet?', title='', choices=('User Defined', 'Parent Folder(default)', 'Same Folder(not recommended)'), image=None)

    if save == 0:
        print ("User Input Dialog Opened")
        savepath = None
        while savepath == None:
            savepath = easygui.filesavebox()
        if (savepath[-4:]) != (filetype[-4:]):
            savepath = savepath + (filetype[-4:])
        print ("Saving Sprite Sheet...")
        imgfinal.save(savepath, "png")
    if save == 1:
        print ("Saving Sprite Sheet...")
        imgfinal.save("../sss_result.png", "png")
    if save == 2:
        print ("Saving Sprite Sheet...")
        imgfinal.save("sss_result.png", "png")

    print ("All done.")

    time.sleep(0.7)

    restart = easygui.indexbox(msg='Compile another sprite sheet?', title='', choices=('No(Exit)', 'Yes(Restart)'), image=None)

    if restart == 0:
        exit
