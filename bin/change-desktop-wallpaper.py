#!/usr/bin/env python3
#This script changes desktop wallpaper

import os
import re
import time
import random
import subprocess
import platform
import ctypes

time.sleep(10)

home_dir = os.path.expanduser('~')
image_dirs = [r'',] #wallpaper directories
exclusions = [] #excluded files and directories
min_size = 10 #10 KiB
patterns = [r'^.*\.[Jj][Pp][Ee]?[Gg]$', r'^.*\.[Pp][Nn][Gg]$', r'^.*\.[Bb][Mm][Pp]$']
log_path = os.path.join(home_dir,'.change-desktop-wallpaper', '.prev_wallpapers.log')
images = []
DESKTOPS = ["windows","openbox", "xfce4"]

def get_desktop():
    desktop_session = os.environ.get("DESKTOP_SESSION")
    if desktop_session is None:
        if platform.system() is None:
            return "unknown"
        else:
            return platform.system().lower()
    else:
        desktop_session = desktop_session.lower()

    if "xfce" in desktop_session or desktop_session.startswith("xubuntu"): #xfce4
        return "xfce4"
    elif "openbox" in desktop_session: #openbox
        return "openbox"
    else:
        return "other"

def get_trimmed(f):
    lines = [(l.strip() + '\n') for l in f.readlines() if l.strip() and os.path.isfile(l.strip())]
    f.seek(0)
    for line in lines:
        f.write(line)
    f.truncate()
    return [line[:-1] for line in lines]

def is_image(name):
    for pattern in patterns:
        if re.match(pattern,name):
            return True
    return False

def is_small(name):
    return ((os.path.getsize(os.path.realpath(name)) >> 10) < min_size)  #Smaller than min_size
	
def is_in_dir(file_path,directory):
    return os.path.realpath(file_path).startswith(os.path.realpath(directory) + os.sep)

def is_excluded(name):
    for exclusion in exclusions:
        if os.path.realpath(name) == os.path.realpath(exclusion):
            return True
        if is_in_dir(name,exclusion):
            print(name)
            return True
    return False

desktop = get_desktop()

if not desktop in DESKTOPS:
    exit(1)

if 'image_dirs' in locals(): #if image_dirs local variable exist
    for image_dir in image_dirs:
        if image_dir:
            break
    else: #if image_dirs variable only has empty strings
        image_dirs = [os.path.join(home_dir,'Pictures')]
else:
    image_dirs = [os.path.join(home_dir,'Pictures')]

for image_dir in image_dirs:
    if os.path.exists(os.path.realpath(image_dir)):
        for root, directories, file_names in os.walk(os.path.realpath(image_dir)):
            for file_name in file_names:
                if is_image(os.path.join(root,file_name)):
                    if not is_small(os.path.join(root,file_name)):
                        if not is_excluded(os.path.join(root,file_name)):
                            images.append(os.path.realpath(os.path.join(root,file_name)))

images = list(set(images)) #removing duplicates

if len(images) == 0:
    exit(2);

if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))

if os.path.isfile(log_path):
    with open(log_path , 'r+') as log:
        previous_images = get_trimmed(log)
        if len(previous_images) > 0:
            if len(previous_images) < 1001 and len(set(images) - set(previous_images)) > 0:
                for image in previous_images:
                    if image in images:
                        images.remove(image)
            else:
                if previous_images[len(previous_images) - 1] in images:
                    images.remove(previous_images[len(previous_images) - 1])
                log.seek(0)
        else:
            log.seek(0)
        image = images[random.randint(0,len(images) - 1)]
        log.write(image + '\n')
        log.truncate()
else:
    with open(log_path,"w") as log:
        image = images[random.randint(0,len(images) - 1)]
        log.write(image + '\n')

if desktop == "windows":
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0) #SystemParametersInfoA in Python2
if desktop == "xfce4":
    args0 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace1/last-image", "-s", image]
    args1 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace1/image-style", "-s", "5"]
    args2 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-s", "true"]
    subprocess.Popen(args0)
    subprocess.Popen(args1)
    subprocess.Popen(args2)
    args = ["xfdesktop","--reload"]
    subprocess.Popen(args)
elif desktop == "openbox":
    args = ["/usr/bin/feh", "-q", "--bg-fill", image]
    subprocess.Popen(args)

log.close()

exit(0)
