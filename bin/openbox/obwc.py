#!/usr/bin/env python3

#This script changes desktop wallpaper with feh

import os
import re
import time
import random

time.sleep(15)
homedir=os.path.expanduser('~')
logfilename =''.join([homedir,'/bin/openbox/tmp/.prev_wallpapers.log'])
patterns=['^.*\.[Jj][Pp][Ee]?[Gg]$','^.*\.[Pp][Nn][Gg]$','^.*\.[Bb][Mm][Pp]$']
images=[]
for root, directories, filenames in os.walk(''.join([homedir,'/Pictures/Desktop/'])):
    for filename in filenames:
        for pattern in patterns:
            if re.match(pattern,filename):
                if (os.path.getsize(os.path.realpath(os.path.join(root,filename))) >> 10) >= 10:  #at least 10kiB
                    images.append(os.path.realpath(os.path.join(root,filename)))
                break
if len(images)== 0:
    exit(1);
if os.path.isfile(logfilename):
    with open(logfilename , 'r+') as logfile:
        previousimages = logfile.read().split('\n')
        if len(previousimages) < min(len(images),1000): 
            for image in previousimages:
                if image in images:
                    images.remove(image)
            if len(previousimages) > 0:
                logfile.write('\n')
        else:
             logfile.seek(0)
        image=images[random.randint(0,len(images)-1)]
        logfile.write(image)
        logfile.truncate()
else:
   with open(logfilename,"w") as logfile:
        image=images[random.randint(0,len(images)-1)]
        logfile.write(image)
command='/usr/bin/feh -q --bg-fill \'{}\''.format(image)
os.system(command)
logfile.close()
