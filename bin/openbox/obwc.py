#!/usr/bin/env python3
#changing wallpaper of openbox

import os
import glob
import time
import random

time.sleep(15)
homedir=os.path.expanduser('~')
logfilename =''.join([homedir,'/bin/openbox/tmp/.lastimage.txt'])
images = glob.glob(''.join([homedir,'/Pictures/Desktop/*.jpg']))
if len(images)== 0:
    exit(1);
if os.path.isfile(logfilename):
    with open(logfilename , 'r+') as logfile:
        lastimagename = logfile.read().replace('\n', '')
        if lastimagename in images:
            images.remove(lastimagename)
        image=images[random.randint(0,len(images)-1)]
        logfile.seek(0)
        logfile.write(image)
        logfile.truncate()
else:
   with open(logfilename,"w") as logfile:
        image=images[random.randint(0,len(images)-1)]
        logfile.write(image)
command='/usr/bin/feh --bg-fill \'{}\''.format(image)
os.system(command)
logfile.close()
