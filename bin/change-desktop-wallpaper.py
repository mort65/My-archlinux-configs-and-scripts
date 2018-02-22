#!/usr/bin/env python3
#This script changes desktop wallpaper

import os
import re
import time
import random
import subprocess

time.sleep(15)

homedir=os.path.expanduser('~')
logfilename =''.join([homedir, '/.prev_wallpapers.log'])
patterns=[r'^.*\.[Jj][Pp][Ee]?[Gg]$', r'^.*\.[Pp][Nn][Gg]$', r'^.*\.[Bb][Mm][Pp]$']
desktops=["openbox", "xfce4"]
images=[]

def getdesktop():
    desktop_session = os.environ.get("DESKTOP_SESSION")
    if desktop_session is None:
        return "unknown"
    else:
        desktop_session = desktop_session.lower()
    
    if "xfce" in desktop_session or desktop_session.startswith("xubuntu"): #xfce4
        return "xfce4"
    elif "openbox" in desktop_session: #openbox
        return "openbox"
    else:
        return "other"
    
def gettrimmed(f):
    lines=[(l.strip()+'\n') for l in f.readlines() if l.strip() and os.path.isfile(l.strip())]
    f.seek(0)
    for line in lines:
        f.write(line)
    f.truncate()
    return [line[:-1] for line in lines]

def ispic(name):
    for pattern in patterns:
        if re.match(pattern,name):
            return True
    return False

def issmall(name):
    return ((os.path.getsize(os.path.realpath(os.path.join(root,name))) >> 10) < 10)  #Smaller than 10 kiB

desktop = getdesktop()

if not desktop in desktops:
    exit(1)

for root, directories, filenames in os.walk(''.join([homedir,'/Pictures/Desktop/'])):
    for filename in filenames:
        if ispic(filename) and not issmall(filename):
            images.append(os.path.realpath(os.path.join(root,filename)))

if len(images)== 0:
    exit(1);

if os.path.isfile(logfilename):
    with open(logfilename , 'r+') as logfile:
        previousimages=gettrimmed(logfile)
        if len(previousimages) > 0: 
            if len(previousimages) < min(len(images),1001):
                for image in previousimages:
                    if image in images:
                        images.remove(image)
            else:
                if previousimages[len(previousimages)-1] in images:
                    images.remove(previousimages[len(previousimages)-1])
                logfile.seek(0)
        else:
            logfile.seek(0)
        image=images[random.randint(0,len(images)-1)]
        logfile.write(image+'\n')
        logfile.truncate()
else:
    with open(logfilename,"w") as logfile:
        image=images[random.randint(0,len(images)-1)]
        logfile.write(image+'\n')

if desktop == "xfce4":
    args0 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace1/last-image", "-s", image]
    args1 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace1/image-style", "-s", "3"]
    args2 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-s", "true"]
    subprocess.Popen(args0)
    subprocess.Popen(args1)
    subprocess.Popen(args2)
    args = ["xfdesktop","--reload"]
    subprocess.Popen(args)
elif desktop == "openbox":
    args = ["/usr/bin/feh", "-q", "--bg-fill", image]
    subprocess.Popen(args)

logfile.close()
