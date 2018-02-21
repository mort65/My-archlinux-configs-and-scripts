#!/usr/bin/env python3
#This script changes desktop wallpaper with feh

import os
import re
import time
import random

time.sleep(15)

homedir=os.path.expanduser('~')
logfilename =''.join([homedir,'/bin/openbox/tmp/.prev_wallpapers.log'])
patterns=[r'^.*\.[Jj][Pp][Ee]?[Gg]$',r'^.*\.[Pp][Nn][Gg]$',r'^.*\.[Bb][Mm][Pp]$']
images=[]

def trim(f):
    lines=[(l.strip()+'\n') for l in f.readlines() if l.strip() and os.path.isfile(l.strip())]
    if len(lines) > 0:
        lines[len(lines)-1]=lines[len(lines)-1].rstrip() #remove last \n
    f.seek(0)
    for line in lines:
        f.write(line)
    f.truncate()
    f.seek(0)

def ispic(name):
    for pattern in patterns:
        if re.match(pattern,name):
            return True
    return False

def issmall(name):
    return ((os.path.getsize(os.path.realpath(os.path.join(root,name))) >> 10) < 10)  #smaller than 10 kiB
    
for root, directories, filenames in os.walk(''.join([homedir,'/Pictures/Desktop/'])):
    for filename in filenames:
        if ispic(filename) and not issmall(filename):
            images.append(os.path.realpath(os.path.join(root,filename)))

if len(images)== 0:
    exit(1);

if os.path.isfile(logfilename):
    with open(logfilename , 'r+') as logfile:
        trim(logfile)
        previousimages = logfile.read().split('\n')
        if len(previousimages) > 0: 
            if len(previousimages) < min(len(images),1001):
                for image in previousimages:
                    if image in images:
                        images.remove(image)
                logfile.write('\n')
            elif previousimages[len(previousimages)-1] in images:
                images.remove(previousimages[len(previousimages)-1])
                logfile.seek(0)
        else:
            logfile.seek(0)
        image=images[random.randint(0,len(images)-1)]
        logfile.write(image)
        logfile.truncate()
else:
   with open(logfilename,"w") as logfile:
        image=images[random.randint(0,len(images)-1)]
        logfile.write(image)

os.system('/usr/bin/feh -q --bg-fill \'{}\''.format(image))
logfile.close()
