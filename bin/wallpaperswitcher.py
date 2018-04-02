#!/usr/bin/env python3
#This script changes _desktop wallpaper

import os
import re
import random
import subprocess
import platform
import ctypes
import time

class wallpaperswitcher(object):
    '''This class changes desktop wallpaper.'''
    _home_dir = os.path.expanduser('~')
    _patterns = [r'^.*\.[Jj][Pp][Ee]?[Gg]$', r'^.*\.[Pp][Nn][Gg]$', r'^.*\.[Bb][Mm][Pp]$']
    _log_path = os.path.join(_home_dir,'.wallpaperswitcher', '.prev_wallpapers')
    _PLATFORMS = ("windows","linux")
    _DESKTOPS = ("i3", "openbox", "qtile", "xfce4", "plasma", "gnome")
    _platform = platform.system().lower()
    _desktop = ''
    _images = []
    _image_dirs = []
    _exclusions = []
    _min_size = []
    _interval = None

    def __init__(self,Image_Dirs=[os.path.join(_home_dir,'Pictures'),],
                 Exclusions = [], Min_Size=10.0,Interval=None):
        self._image_dirs = Image_Dirs
        self._exclusions = Exclusions
        self._min_size = Min_Size
        self._interval = Interval

    def _get_trimmed(self,f):
        lines = [(l.strip() + '\n') for l in f.readlines() if l.strip() and (l.strip() in self._images)]
        f.seek(0)
        for line in lines:
            f.write(line)
        f.truncate()
        return [line[:-1] for line in lines]

    def _is_image(self,name):
        for pattern in self._patterns:
            if re.match(pattern,name):
                return True
        return False

    def _is_small(self,name):
        return ((os.path.getsize(os.path.realpath(name)) >> 10) < self._min_size)
    
    def _is_same_file(self,name,file_name):
        if self._platform == "windows":
            if os.path.realpath(name).upper() == file_name.upper():
                return True
            elif os.path.basename(name).upper() == file_name.upper():
                return True
        elif self._platform == "linux":
            if os.path.realpath(name) == file_name:
                return True
            elif os.path.basename(name) == file_name:
                return True
        return False
    
    def _is_in_dir(self,file_path,dir_name):
        if self._platform == "windows":
            if os.path.realpath(file_path).upper().startswith(os.path.realpath(dir_name).upper() + os.sep):
                return True
        elif self._platform == "linux":
            if os.path.realpath(file_path).startswith(os.path.realpath(dir_name) + os.sep):
                return True
        return False
    
    def _is_in_drive(self,file_path,drive_name):
        if self._platform == "windows":
            if os.path.splitdrive(os.path.realpath(drive_name))[0]:
                if os.path.splitdrive(os.path.realpath(file_path))[0].upper() == drive_name.upper():
                    return True
                elif ( os.path.splitdrive(os.path.realpath(file_path))[0].upper() + os.sep ) == drive_name.upper():
                    return True
        return False
                
    def _is_excluded(self,name):
        for exclusion in self._exclusions:
            if self._is_same_file(name,exclusion):
                return True
            elif self._is_in_dir(name,exclusion):
                return True
            elif self._is_in_drive(name,exclusion):
                return True
        return False

    def _check_images(self):
        if len(self._image_dirs) > 0:
            for image_dir in self._image_dirs:
                if image_dir:
                    break
            else:
                self._image_dirs=[os.path.join(_home_dir,'Pictures'),]
        else:
            self._image_dirs=[os.path.join(_home_dir,'Pictures'),]

        for image_dir in self._image_dirs:
            if os.path.exists(os.path.realpath(image_dir)):
                for root, directories, file_names in os.walk(os.path.realpath(image_dir)):
                    for file_name in file_names:
                        if self._is_image(os.path.join(root,file_name)):
                            if not self._is_small(os.path.join(root,file_name)):
                                if not self._is_excluded(os.path.join(root,file_name)):
                                    self._images.append(os.path.realpath(os.path.join(root,file_name)))

        self._images = list(set(self._images)) #removing duplicates
        
        if len(self._images) == 0:
           return False
        return True
        
    def _get_desktop(self):
        desktop_session = os.environ.get("DESKTOP_SESSION")
        if desktop_session is None:
            self._desktop = "unknown"
        else:
            desktop_session = desktop_session.lower()
            if "xfce" in desktop_session or "xubuntu" in desktop_session:
                self._desktop = "xfce4"
            elif "plasma" in desktop_session or "openbox-kde" in desktop_session:
                self._desktop = "plasma"
            elif "gnome" in desktop_session:
                self._desktop = "gnome"
            elif "i3" in desktop_session:
                self._desktop = "i3"
            elif "qtile" in desktop_session:
                self._desktop = "qtile"
            elif "openbox" in desktop_session:
                self._desktop = "openbox"
            else:
                self._desktop = "other"
        if self._desktop in self._DESKTOPS:
            return True
        return False

    def _check_platform(self):
        if self._platform in self._PLATFORMS:
            if self._platform == "linux":
                self._get_desktop()
        else:
            return False
        return True

    def _select_image(self):
        image=''
        if not os.path.exists(os.path.dirname(self._log_path)):
            os.makedirs(os.path.dirname(self._log_path))

        if os.path.isfile(self._log_path):
            with open(self._log_path , 'r+') as log:
                previous_images = self._get_trimmed(log)
                if len(previous_images) > 0:
                    if len(previous_images) < 10001 and len(set(self._images) - set(previous_images)) > 0:
                        for image in previous_images:
                            self._images.remove(image)
                    else:
                        if len(self._images) > 1:
                            self._images.remove(previous_images[len(previous_images) - 1])
                        log.seek(0)
                else:
                    log.seek(0)
                image = self._images[random.randint(0,len(self._images) - 1)]
                log.write(image + '\n')
                log.truncate()
        else:
            with open(self._log_path,"w") as log:
                image = self._images[random.randint(0,len(self._images) - 1)]
                log.write(image + '\n')
        log.close()
        return image


    def _set_wallpaper(self,image):
        if os.path.exists(image):
            if self._platform == "windows":
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)
            elif self._platform == "linux":
                if  self._desktop == "xfce4":
                    args0 = ["/usr/bin/xfconf-query", "-c", "xfce4-_desktop", "-p", "/backdrop/screen0/monitor0/workspace1/last-image", "-s", image]
                    args1 = ["/usr/bin/xfconf-query", "-c", "xfce4-_desktop", "-p", "/backdrop/screen0/monitor0/workspace1/image-style", "-s", "5"]
                    args2 = ["/usr/bin/xfconf-query", "-c", "xfce4-_desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-s", "true"]
                    subprocess.Popen(args0)
                    subprocess.Popen(args1)
                    subprocess.Popen(args2)
                    args = ["xfdesktop","--reload"]
                    subprocess.Popen(args)
                elif  self._desktop == "plasma":
                    script0 = "var allDesktops = desktops(); for (i=0;i<allDesktops.length;i++) { d=allDesktops[i]; d.wallpaperPlugin = \"org.kde.image\"; d.currentConfigGroup=Array(\"Wallpaper\",\"org.kde.image\",\"General\"); d.writeConfig(\"Image\",\"file://" + image + "\")}"
                    args0 = ["/usr/bin/qdbus", "org.kde.plasmashell","/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", script0]
                    subprocess.Popen(args0)
                elif self._desktop == "gnome":
                    args = ["gsettings", "set", "org.gnome._desktop.background", "picture-uri", "file://{}".format(image)]
                    subprocess.Popen(args)
                elif self._desktop == "openbox" or self._desktop == "i3" or self._desktop == "qtile":
                    args = ["/usr/bin/feh", "-q", "--bg-fill", image]
                    subprocess.Popen(args)

    def set_wallpaper(self,image):
        self._set_wallpaper(image)

    def _run(self):
        if self._check_platform():
            if self._check_images():
                self._set_wallpaper(self._select_image())
        else:
            exit(2)

    def start(self):
        if self._interval is None:
            self._run()
        else:
            if ( self._interval < 0 ) or ( self._interval > 0 and self._interval < 1 ):
                raise ValueError
            self._interval = int(self._interval)
            if self._interval == 0:
                self._run()
            else:
                starttime = time.time()
                try:
                    while True:
                        self._run()
                        time.sleep(self._interval - ((time.time() - starttime) % self._interval))
                except KeyboardInterrupt:
                    print("\nManual break by User")
                except Exception:
                    exit(1)

if __name__ == "__main__":
    pic_dirs = []
    exceptions = []
    min_size_in_kb = 10.0
    interval_in_sec = None

    w = wallpaperswitcher(pic_dirs,exceptions,min_size_in_kb,interval_in_sec)
    w.start()
