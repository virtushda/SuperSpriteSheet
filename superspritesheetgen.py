from PIL import Image

import easygui
import math

opath = easygui.fileopenbox()
fsize = easygui.integerbox(msg='Frame Size?', lowerbound=4, upperbound=2048)
fcount = easygui.integerbox(msg='How many frames?', lowerbound=1, upperbound=1024)
fcountsqr = math.sqrt(fcount)
colcount = (fcountsqr)
    
img = Image.open(opath)
    
img = img.resize((fsize,fsize))
img.c = img.copy()
print (img.c)

#outimg = img.resize((2024, 2024))
#print (outimg)
