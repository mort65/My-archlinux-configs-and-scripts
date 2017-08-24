#!/usr/bin/env python3
#changing wallpaper of workspace1
import os
import glob
import time

time.sleep(5)
home_Dir=os.path.expanduser('~')
images = glob.glob(home_Dir+"/.i3wm-wallpapers/*")
image=''

for f in images:
    if os.path.splitext(os.path.basename(f))[0]=='1':
        image=f

command='/usr/bin/feh --bg-scale \'{}\''.format(image)

os.system(command)
