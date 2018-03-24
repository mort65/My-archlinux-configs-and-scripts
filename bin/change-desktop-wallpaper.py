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
image_dirs = [r'',] #wallpaper directories (default: ~/Pictures)
exclusions = [] #excluded files and directories
min_size = 10 #KiB
patterns = [r'^.*\.[Jj][Pp][Ee]?[Gg]$', r'^.*\.[Pp][Nn][Gg]$', r'^.*\.[Bb][Mm][Pp]$']
log_path = os.path.join(home_dir,'.change-desktop-wallpaper', '.prev_wallpapers.log')
images = []
PLATFORMS = ("windows","linux")
DESKTOPS = ("openbox", "xfce4", "plasma")
platform = platform.system().lower()
desktop = ''

def get_desktop():
    desktop_session = os.environ.get("DESKTOP_SESSION")
    if desktop_session is None:
        return "unknown"
    else:
        desktop_session = desktop_session.lower()
    if "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
        return "xfce4"
    elif "openbox" in desktop_session:
        return "openbox"
    elif "plasma" in desktop_session:
        return "plasma"
    else:
        return "other"

def get_trimmed(f):
    lines = [(l.strip() + '\n') for l in f.readlines() if l.strip() and (l.strip() in images)]
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
    return ((os.path.getsize(os.path.realpath(name)) >> 10) < min_size)
    
def is_same_file(name,file_name):
    if platform == "windows":
        if os.path.realpath(name).upper() == file_name.upper():
            return True
        elif os.path.basename(name).upper() == file_name.upper():
            return True
    elif platform == "linux":
        if os.path.realpath(name) == file_name:
            return True
        elif os.path.basename(name) == file_name:
            return True
    return False
    
def is_in_dir(file_path,dir_name):
    if platform == "windows":
        if os.path.realpath(file_path).upper().startswith(os.path.realpath(dir_name).upper() + os.sep):
            return True
    elif platform == "linux":
        if os.path.realpath(file_path).startswith(os.path.realpath(dir_name) + os.sep):
            return True
    return False
    
def is_in_drive(file_path,drive_name):
    if platform == "windows":
        if os.path.splitdrive(os.path.realpath(drive_name))[0]:
            if os.path.splitdrive(os.path.realpath(file_path))[0].upper() == drive_name.upper():
                return True
            elif ( os.path.splitdrive(os.path.realpath(file_path))[0].upper() + os.sep ) == drive_name.upper():
                return True
    return False
                
def is_excluded(name):
    for exclusion in exclusions:
        if is_same_file(name,exclusion):
            return True
        elif is_in_dir(name,exclusion):
            return True
        elif is_in_drive(name,exclusion):
            return True
    return False

if platform in PLATFORMS:
    if platform == "linux":
        desktop = get_desktop()
        if not desktop in DESKTOPS:
            exit(1)
else:
    exit(1)
    
if len(image_dirs) > 0:
    for image_dir in image_dirs:
        if image_dir:
            break
    else:
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
                    images.remove(image)
            else:
                if len(images) > 1:
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

if platform == "windows":
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)
elif platform == "linux":
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
    elif desktop == "plasma":
        script0 = "var allDesktops = desktops(); for (i=0;i<allDesktops.length;i++) { d=allDesktops[i]; d.wallpaperPlugin = \"org.kde.image\"; d.currentConfigGroup=Array(\"Wallpaper\",\"org.kde.image\",\"General\"); d.writeConfig(\"Image\",\"file://" + image + "\")}"
        args0 = ["/usr/bin/qdbus", "org.kde.plasmashell","/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", "{}".format(script0)]
        subprocess.Popen(args0)
log.close()

exit(0)
