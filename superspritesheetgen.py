from PIL import Image

import easygui
import math

opath = easygui.fileopenbox(title='Pick an image sequence!')
tsize = easygui.integerbox(msg='Texture Size?', lowerbound=16, upperbound=4094)
#fcount = easygui.integerbox(msg='How many frames?', lowerbound=1, upperbound=1024)
#fcountsqr = math.sqrt(fcount)
#colcount = math.ceil(fcountsqr)
#print (colcount)
    
img = Image.open(opath)
    
img = img.resize((tsize,tsize))
img.c = img.copy()
print (img.c)

#outimg = img.resize((2024, 2024))
#print (outimg)
