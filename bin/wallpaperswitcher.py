#!/usr/bin/env python3
#This script changes desktop wallpaper

import os
import re
import random
import subprocess
import platform
import ctypes
import time
import sys
from operator import itemgetter

class wallpaperswitcher(object):
    '''This class changes desktop wallpaper.'''
    _home_dir = os.path.expanduser('~')
    initialized = False
    cleanedup = False
            
    def __init__(self,Image_Dirs=[os.path.join(_home_dir,'Pictures'),],
                 Exclusions = [], Min_Size=10.0,Image_Order=("Random",None),Interval=None):
        
        self._patterns = [r'^.*\.[Jj][Pp][Ee]?[Gg]$', r'^.*\.[Pp][Nn][Gg]$', r'^.*\.[Bb][Mm][Pp]$']
        self._log_path = os.path.join(self._home_dir,'.wallpaperswitcher', '.prev_wallpapers')
        self._PLATFORMS = ("windows","linux")
        self._DESKTOPS = ("i3", "openbox", "qtile", "xfce4", "plasma", "gnome", "budgie", "lxde",)
        self._ORDERS = {"random":(None,), "name":("ascend","descend"), "size":("ascend","descend",),
        "date":("ascend","descend",)}
        self._platform = platform.system().lower()
        self._desktop = ''
        self._images = []
        self._image_dirs = []
        self._exclusions = []
        self._min_size = []
        self._interval = None
        self._fh = None
        self._images_limit = 1000000
        
        try:
            if type(Image_Dirs) == type(self._image_dirs):
                for i in Image_Dirs:
                    if not (type(i) == type('')):
                        raise ValueError("Invalid value: {}".format("Image_Dirs"))
                self._image_dirs = Image_Dirs
            else:
                raise ValueError("Invalid value: {}".format("Image_Dirs"))
            
            if type(Exclusions) == type(self._exclusions):
                for i in Exclusions:
                    if not (type(i) == type('')):
                        raise ValueError("Invalid value: {}".format("Exclusions"))
                self._exclusions = Exclusions
            else:
                raise ValueError("Invalid value: {}".format("Exclusions"))
            
            if (type(Min_Size) == type(0.0) or
            type(Min_Size) == type(0)):
                self._min_size = Min_Size
            else:
                raise ValueError("Invalid value: {}".format("Min_Size"))
            
            if (type(Interval) == type(0.0) or
            type(Interval) == type(0) or
            type(Interval) == type(None)):
                self._interval = Interval
            else:
                raise ValueError("Invalid value: {}".format("Interval"))
            
            if len(Image_Order) == 2:
                if (Image_Order[0] in self._ORDERS.keys()):
                    if(Image_Order[1] in self._ORDERS[Image_Order[0]]):
                        self._order = Image_Order
                    else:
                        raise ValueError("Invalid value: {}".format("Image_Order"))
                else:
                    raise ValueError("Invalid value: {}".format("Image_Order"))
            else:
                raise ValueError("Invalid value: {}".format("Image_Order"))
            
            if not os.path.exists(os.path.dirname(self._log_path)):
                os.makedirs(os.path.dirname(self._log_path))
            
            self._fh = os.path.join(self._home_dir,'.wallpaperswitcher','.lock')
            
            if not self._check_single_instance():
                print("Another instance is already running, quitting.")
                exit(0)
            
            self.initialized = True
        except ValueError as err:
            print(err)
            exit(1)
    

    def __del__(self):
        if self.initialized:
            if not self.cleanedup:
                self._clean_up()
            
        
    def _clean_up(self):
        if self._platform == "linux":
            import fcntl
            fcntl.lockf(self.fp, fcntl.LOCK_UN)
            if os.path.isfile(self._fh):
                os.unlink(self._fh)
        elif self._platform == 'windows':
            if hasattr(self, 'fd'):
                os.close(self.fd)
                os.unlink(self._fh)
        self.cleanedup = True

    def _check_single_instance(self):
        if self._platform == "windows":
            try:
                if os.path.exists(self._fh):
                     os.unlink(self._fh)
                self.fd = os.open(self._fh, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except OSError:
                t, v, b = sys.exc_info()
                if v.errno == 13:
                   return False
                raise
            return True
        else:
            import fcntl
            self.fp = open(self._fh, 'w')
            self.fp.flush()
            try:
                fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
               return False
            return True

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
                self._image_dirs=[os.path.join(self._home_dir,'Pictures'),]
        else:
            self._image_dirs=[os.path.join(self._home_dir,'Pictures'),]

        for image_dir in self._image_dirs:
            if os.path.exists(os.path.realpath(image_dir)):
                for root, directories, file_names in os.walk(os.path.realpath(image_dir)):
                    for file_name in file_names:
                        if len(self._images) < self._images_limit:
                            if self._is_image(os.path.join(root,file_name)):
                                if not self._is_small(os.path.join(root,file_name)):
                                    if not self._is_excluded(os.path.join(root,file_name)):
                                        self._images.append(os.path.realpath(os.path.join(root,file_name)))
                        else:
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
        
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
            elif "budgie" in desktop_session:
                self._desktop = "budgie"
            elif "lxde" in desktop_session:
                self._desktop = "lxde"
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
                return self._get_desktop()
            else:
                return True
        return False

    def _get_next_image(self):
        next_image = ''
        if self._order[0] == "random":
            next_image = self._images[random.randint(0,len(self._images) - 1)]
        elif self._order[0] == "name":
            images_dict = {}
            ordered_images = []
            for i in self._images:
                images_dict[i] = os.path.basename(i).lower()
            if self._order[1] == "ascend":
                ordered_images = sorted(images_dict.items(),key=itemgetter(1))
            elif self._order[1] == "descend": 
                ordered_images = sorted(images_dict.items(),key=itemgetter(1),reverse=True)
            next_image = ordered_images[0][0]
        elif self._order[0] == "size":
            images_dict = {}
            ordered_images = []
            for i in self._images:
                images_dict[i] = os.path.getsize(i)
            if self._order[1] == "ascend":
                ordered_images = sorted(images_dict.items(),key=itemgetter(1))
            elif self._order[1] == "descend": 
                ordered_images = sorted(images_dict.items(),key=itemgetter(1),reverse=True)
            next_image = ordered_images[0][0]
        elif self._order[0] == "date":
            images_dict = {}
            ordered_images = []
            for i in self._images:
                images_dict[i] = os.path.getmtime(i)
            if self._order[1] == "ascend":
                ordered_images = sorted(images_dict.items(),key=itemgetter(1))
            elif self._order[1] == "descend": 
                ordered_images = sorted(images_dict.items(),key=itemgetter(1),reverse=True)
            next_image = ordered_images[0][0]
                
        return next_image
        
    def _select_image(self):
        image=''
        if os.path.isfile(self._log_path):
            with open(self._log_path , 'r+') as log:
                previous_images = self._get_trimmed(log)
                if len(previous_images) > 0:
                    if len(set(self._images) - set(previous_images)) > 0:
                        for image in previous_images:
                            self._images.remove(image)
                    else:
                        if len(self._images) > 1:
                            self._images.remove(previous_images[len(previous_images) - 1])
                        log.seek(0)
                else:
                    log.seek(0)
                image = self._get_next_image()
                log.write(image + '\n')
                log.truncate()
        else:
            with open(self._log_path,"w") as log:
                image = self._get_next_image()
                log.write(image + '\n')
        log.close()
        return image

    def _set_wallpaper(self,image):
        if os.path.exists(image):
            if self._platform == "windows":
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)
            elif self._platform == "linux":
                if  self._desktop == "xfce4":
                    args0 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace1/last-image", "-s", image]
                    args1 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace1/image-style", "-s", "5"]
                    args2 = ["/usr/bin/xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-s", "true"]
                    subprocess.Popen(args0)
                    subprocess.Popen(args1)
                    subprocess.Popen(args2)
                    args = ["xfdesktop","--reload"]
                    subprocess.Popen(args)
                elif  self._desktop == "plasma":
                    script0 = "var allDesktops = desktops(); for (i=0;i<allDesktops.length;i++) { d=allDesktops[i]; d.wallpaperPlugin = \"org.kde.image\"; d.currentConfigGroup=Array(\"Wallpaper\",\"org.kde.image\",\"General\"); d.writeConfig(\"Image\",\"file://" + image + "\")}"
                    args0 = ["/usr/bin/qdbus", "org.kde.plasmashell","/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", script0]
                    subprocess.Popen(args0)
                elif self._desktop == "gnome" or self._desktop == "budgie":
                    args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://{}".format(image)]
                    subprocess.Popen(args)
                elif self._desktop == "lxde":
                    args = ["/usr/bin/pcmanfm", "--set-wallpaper={}".format(image)]
                    subprocess.Popen(args)
                elif (self._desktop == "openbox" or self._desktop == "i3" or self._desktop == "qtile"):
                    args = ["/usr/bin/feh", "-q", "--bg-fill", image]
                    subprocess.Popen(args)

    def set_wallpaper(self,image):
        self._set_wallpaper(image)

    def _run(self):
        if self._check_platform():
            if self._check_images():
                self._set_wallpaper(self._select_image())
        else:
            if self._platform == "linux":
                print("Unsupported desktop")
            else:
                print("Unsupported platform")
            exit(2)

    def start(self):
        try:
            if self._interval is None or (self._interval == 0):
                self._run()
            elif self._interval < 0 or (self._interval > 0 and self._interval < 1):
                raise ValueError("Interval must be 0 or >=1")
            else:
                starttime = time.time()
                try:
                    while True:
                        self._run()
                        time.sleep(self._interval - ((time.time() - starttime) % self._interval))
                except KeyboardInterrupt:
                    exit(0)
        finally:
            if not self.cleanedup:
                self._clean_up()
            
if __name__ == "__main__":
    image_dirs = []
    exclusions = []
    min_size_in_kb = 10.0
    image_order = ("random",None)
    interval_in_sec = None
    
    w = wallpaperswitcher( Image_Dirs = image_dirs, Exclusions = exclusions, 
    Min_Size = min_size_in_kb, Image_Order = image_order, Interval = interval_in_sec )
    w.start()
