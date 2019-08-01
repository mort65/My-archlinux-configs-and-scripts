#!/usr/bin/env python3
# This script changes desktop wallpaper

import os
import re
import random
import subprocess
import platform
import ctypes
import time
import sys


class WallpaperSwitcher:
    """This class changes desktop wallpaper."""
    _home_dir = os.path.expanduser('~')
    initialized = False
    cleaned_up = False

    def __init__(
            self,
            image_dirs=(
                os.path.join(
                    _home_dir,
                    'Pictures'),
            ),
        exclusions=(),
        min_size=10.0,
        image_order=(
                "random",
                None),
            interval=None,
            initial_image=None):

        self._patterns = [
            r'^.*\.[Jj][Pp][Ee]?[Gg]$',
            r'^.*\.[Pp][Nn][Gg]$',
            r'^.*\.[Bb][Mm][Pp]$']
        self._log_path = os.path.join(
            self._home_dir,
            '.wallpaper-switcher',
            '.prev_wallpapers')
        self._PLATFORMS = ("windows", "linux")
        self._DESKTOPS = (
            "i3",
            "openbox",
            "qtile",
            "xfce4",
            "plasma",
            "gnome",
            "budgie",
            "lxde",
            "jwm",
            "dwm",
            "lxqt")
        self._platform = platform.system().lower()
        self._desktop = ''
        self._first_loop = True
        self._ORDERS = {
            "random": (
                None,), "name": (
                "ascend", "descend"), "size": (
                "ascend", "descend",), "date": (
                    "ascend", "descend",)}
        self._images = []
        self._image_dirs = []
        self._exclusions = []
        self._min_size = []
        self._interval = None
        self._fh = None
        self._images_limit = 1000000
        self._new_cycle = True
        self._initial_image = None
        try:
            if isinstance(initial_image, (str, type(None))):
                if initial_image and os.path.exists(initial_image):
                    self._initial_image = os.path.realpath(initial_image)
                else:
                    self._initial_image = None
            else:
                raise ValueError("Invalid value: {}".format("initial_image"))

            if isinstance(image_dirs, (tuple, type(None))):
                if not image_dirs:
                    image_dirs = ()  # set initial_image as wallpaper and exit
                for i in image_dirs:
                    if not isinstance(i, (str, type(None))):
                        raise ValueError(
                            "Invalid value: {}".format("image_dirs"))
                self._image_dirs = image_dirs
            else:
                raise ValueError("Invalid value: {}".format("image_dirs"))

            if isinstance(exclusions, tuple):
                for i in exclusions:
                    if not isinstance(i, str):
                        raise ValueError(
                            "Invalid value: {}".format("exclusions"))
                self._exclusions = exclusions
            else:
                raise ValueError("Invalid value: {}".format("exclusions"))

            if isinstance(min_size, (int, float)):
                self._min_size = min_size
            else:
                raise ValueError("Invalid value: {}".format("min_size"))

            if isinstance(interval, (int, float, type(None))):
                self._interval = interval
            else:
                raise ValueError("Invalid value: {}".format("interval"))

            if len(image_order) == 2:
                if image_order[0] in self._ORDERS.keys():
                    if image_order[1] in self._ORDERS[image_order[0]]:
                        self._order = image_order
                    else:
                        raise ValueError(
                            "Invalid value: {}".format("image_order"))
                else:
                    raise ValueError("Invalid value: {}".format("image_order"))
            else:
                raise ValueError("Invalid value: {}".format("image_order"))
            if not os.path.exists(os.path.dirname(self._log_path)):
                os.makedirs(os.path.dirname(self._log_path))
            if not os.path.exists(self._log_path):
                with open(self._log_path, "w"):
                    pass
            self._fh = os.path.join(
                self._home_dir, '.wallpaper-switcher', '.lock')

            self.initialized = True
        except ValueError as err:
            print(err)
            exit(1)

    def __del__(self):
        if self.initialized:
            if not self.cleaned_up:
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
        self.cleaned_up = True

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

    def _get_trimmed(self, f, images):
        lines = list(set([(l.strip() + '\n') for l in f.readlines()
                          if l.strip() and (not images or (l.strip() in images))]))
        f.seek(0)
        for line in lines:
            f.write(line)
        f.truncate()
        return [line[:-1] for line in lines]

    def _is_image(self, name):
        for pattern in self._patterns:
            if re.match(pattern, name):
                return True
        return False

    def _is_small(self, name):
        return (os.path.getsize(os.path.realpath(name)) >> 10) < self._min_size

    def _is_same_file(self, name, file_name):
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

    def _is_in_dir(self, file_path, dir_name):
        if self._platform == "windows":
            if os.path.realpath(file_path).upper().startswith(
                    os.path.realpath(dir_name).upper() + os.sep):
                return True
        elif self._platform == "linux":
            if os.path.realpath(file_path).startswith(
                    os.path.realpath(dir_name) + os.sep):
                return True
        return False

    def _is_in_drive(self, file_path, drive_name):
        if self._platform == "windows":
            if os.path.splitdrive(os.path.realpath(drive_name))[0]:
                if os.path.splitdrive(os.path.realpath(file_path))[
                        0].upper() == drive_name.upper():
                    return True
                elif (os.path.splitdrive(os.path.realpath(file_path))[0].upper() + os.sep) == drive_name.upper():
                    return True
        return False

    def _is_excluded(self, name):
        for exclusion in self._exclusions:
            if self._is_same_file(name, exclusion):
                return True
            elif self._is_in_dir(name, exclusion):
                return True
            elif self._is_in_drive(name, exclusion):
                return True
        return False

    def _check_image(self, name):
        if self._is_image(name):
            if not self._is_small(name):
                if not self._is_excluded(name):
                    return True
        return False

    def _check_images(self):
        if len(self._images) > 0:
            return True
        self._new_cycle = True
        if len(self._image_dirs) > 0:
            for image_dir in self._image_dirs:
                if image_dir:
                    break
            else:
                self._image_dirs = [os.path.join(self._home_dir, 'Pictures'), ]
        else:
            exit(0)

        for image_dir in self._image_dirs:
            if os.path.exists(os.path.realpath(image_dir)):
                for root, directories, file_names in os.walk(
                        os.path.realpath(image_dir)):
                    for file_name in file_names:
                        if len(self._images) < self._images_limit:
                            if self._check_image(
                                    os.path.join(root, file_name)):
                                self._images.append(os.path.realpath(
                                    os.path.join(root, file_name)))
                        else:
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

        self._images = list(set(self._images))  # removing duplicatesg

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
            elif "lxqt" in desktop_session:
                self._desktop = "lxqt"
            elif "i3" in desktop_session:
                self._desktop = "i3"
            elif "qtile" in desktop_session:
                self._desktop = "qtile"
            elif "openbox" in desktop_session:
                self._desktop = "openbox"
            elif "jwm" in desktop_session:
                self._desktop = "jwm"
            elif "dwm" in desktop_session:
                self._desktop = "dwm"
            else:
                self._desktop = "other"
        if self._desktop in self._DESKTOPS:
            return True
        return False

    def _check_platform(self):
        if not self._first_loop:
            return True
        if self._platform in self._PLATFORMS:
            if self._platform == "linux":
                return self._get_desktop()
            else:
                return True
        return False

    def _get_next_image(self):
        next_image = ''
        ordered_images = []
        if self._order[0] == "random":
            next_image = self._images[random.randint(0, len(self._images) - 1)]
        elif not self._interval or (self._interval and self._new_cycle):
            if self._order[0] == "name":
                images_dict = {}
                for i in self._images:
                    images_dict[i] = os.path.basename(i).lower()
                if self._order[1] == "ascend":
                    ordered_images = sorted(
                        images_dict.items(),
                        key=lambda elem: (
                            elem[1]))
                elif self._order[1] == "descend":
                    ordered_images = sorted(
                        images_dict.items(), key=lambda elem: (
                            elem[1]), reverse=True)
                next_image = ordered_images[0][0]
            elif self._order[0] == "size":
                images_dict = {}
                for i in self._images:
                    images_dict[i] = os.path.getsize(i)
                if self._order[1] == "ascend":
                    ordered_images = sorted(
                        images_dict.items(),
                        key=lambda elem: (
                            elem[1]))
                elif self._order[1] == "descend":
                    ordered_images = sorted(
                        images_dict.items(), key=lambda elem: (
                            elem[1]), reverse=True)
                next_image = ordered_images[0][0]
            elif self._order[0] == "date":
                images_dict = {}
                for i in self._images:
                    images_dict[i] = os.path.getmtime(i)
                if self._order[1] == "ascend":
                    ordered_images = sorted(
                        images_dict.items(),
                        key=lambda elem: (
                            elem[1]))
                elif self._order[1] == "descend":
                    ordered_images = sorted(
                        images_dict.items(), key=lambda elem: (
                            elem[1]), reverse=True)
                next_image = ordered_images[0][0]

            if self._interval:
                self._images = [ordered_images[i][0]
                                for i in range(len(ordered_images))]
        else:
            next_image = self._images[0]
        return next_image

    def _select_image(self):
        if os.path.isfile(self._log_path):
            with open(self._log_path, 'r+') as log:
                if not self._interval or (self._interval and self._new_cycle):
                    previous_images = self._get_trimmed(
                        log, images=self._images)
                    if self._first_loop:
                        if len(previous_images) > 0:
                            if len(set(self._images) -
                                   set(previous_images)) > 0:
                                for image in previous_images:
                                    self._images.remove(image)
                            else:
                                if (self._order[0] == "random") and len(
                                        self._images) > 1:
                                    self._images.remove(
                                        previous_images[len(previous_images) - 1])
                                log.seek(0)
                        else:
                            log.seek(0)
                    else:
                        if (self._order[0] == "random") and len(
                                self._images) > 1 and len(previous_images) > 0:
                            self._images.remove(
                                previous_images[len(previous_images) - 1])
                        log.seek(0)

                else:
                    log.seek(0, 2)

                image = self._get_next_image()
                log.write(image + '\n')
                log.truncate()
        else:
            with open(self._log_path, "w") as log:
                image = self._get_next_image()
                log.write(image + '\n')
        log.close()
        if image:
            try:
                self._images.remove(image)
            except ValueError:
                self._images.clear()
        return image

    def _set_wallpaper(self, image):
        if os.path.exists(image):
            if self._platform == "windows":
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)
            elif self._platform == "linux":
                if self._desktop == "xfce4":
                    args0 = [
                        "/usr/bin/xfconf-query",
                        "-c",
                        "xfce4-desktop",
                        "-p",
                        "/backdrop/screen0/monitor0/workspace1/last-image",
                        "-s",
                        image]
                    args1 = [
                        "/usr/bin/xfconf-query",
                        "-c",
                        "xfce4-desktop",
                        "-p",
                        "/backdrop/screen0/monitor0/workspace1/image-style",
                        "-s",
                        "5"]
                    args2 = [
                        "/usr/bin/xfconf-query",
                        "-c",
                        "xfce4-desktop",
                        "-p",
                        "/backdrop/screen0/monitor0/image-show",
                        "-s",
                        "true"]
                    subprocess.Popen(args0)
                    subprocess.Popen(args1)
                    subprocess.Popen(args2)
                    args = ["xfdesktop", "--reload"]
                    subprocess.Popen(args)
                elif self._desktop == "plasma":
                    script0 = "var allDesktops = desktops(); for (i=0;i<allDesktops.length;i++) { d=allDesktops[i]; " \
                              "d.wallpaperPlugin = \"org.kde.image\"; d.currentConfigGroup=Array(\"Wallpaper\"," \
                              "\"org.kde.image\",\"General\"); d.writeConfig(\"Image\",\"file://" + image + "\")} "
                    args0 = [
                        "/usr/bin/qdbus",
                        "org.kde.plasmashell",
                        "/PlasmaShell",
                        "org.kde.PlasmaShell.evaluateScript",
                        script0]
                    subprocess.Popen(args0)
                elif self._desktop == "gnome" or self._desktop == "budgie":
                    args = [
                        "gsettings",
                        "set",
                        "org.gnome.desktop.background",
                        "picture-uri",
                        "file://{}".format(image)]
                    subprocess.Popen(args)
                elif self._desktop == "lxde":
                    args = [
                        "/usr/bin/pcmanfm",
                        "--set-wallpaper={}".format(image)]
                    subprocess.Popen(args)
                elif self._desktop == "lxqt":
                    args = [
                        "/usr/bin/pcmanfm-qt",
                        "--set-wallpaper={}".format(image)]
                    subprocess.Popen(args)
                elif self._desktop == "openbox" or self._desktop == "i3" or self._desktop == "qtile" or self._desktop == "jwm" or self._desktop == "dwm":
                    args = ["/usr/bin/feh", "-q", "--bg-fill", image]
                    subprocess.Popen(args)
        else:
            self._images.clear()

    def set_wallpaper(self, image):
        self._set_wallpaper(image)

    def _run(self):
        if self._check_platform():
            if self._first_loop and self._initial_image and self._check_image(
                    self._initial_image):
                self._set_wallpaper(self._initial_image)
                with open(self._log_path, 'r+') as log:
                    previous_images = self._get_trimmed(log, images=None)
                    if self._initial_image in previous_images:
                        previous_images.remove(self._initial_image)
                        previous_images.append(self._initial_image)
                        log.seek(0)
                        for image in previous_images:
                            log.write(image + '\n')
                    else:
                        log.seek(0, 2)
                        log.write(self._initial_image + '\n')
                        log.truncate()
                    # else:
                    #    log.seek(0)
            elif self._check_images():
                self._set_wallpaper(self._select_image())
        else:
            if self._platform == "linux":
                print("Unsupported desktop")
            else:
                print("Unsupported platform")
            exit(2)

    def start(self):
        try:
            if not self._check_single_instance():
                print("Another instance is already running, quitting.")
                exit(0)

            if not self._interval:
                self._run()
            elif self._interval < 0 or (0 < self._interval < 1):
                raise ValueError("Interval must be 0 or >=1")
            else:
                start_time = time.time()
                try:
                    while True:
                        self._run()
                        self._first_loop = False
                        self._new_cycle = False
                        time.sleep(
                            self._interval - ((time.time() - start_time) % self._interval))
                except KeyboardInterrupt:
                    exit(0)
        finally:
            if not self.cleaned_up:
                self._clean_up()


if __name__ == "__main__":
    Interval_In_Secs = 0
    Initial_Image_File = None
    Image_Dirs = (None,) #will use ~/Pictures
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):  # set wallpaper the exit
            Initial_Image_File = sys.argv[1]
            Image_Dirs = None
            Interval_In_Secs = 0
        elif os.path.isdir(sys.argv[1]):
            Image_Dirs = (sys.argv[1],)
        else:
            exit(1)

    Exclusions = ()
    Min_Size_In_Kb = 10.0
    Image_Order = ("random", None)

    w = WallpaperSwitcher(
        image_dirs=Image_Dirs,
        exclusions=Exclusions,
        min_size=Min_Size_In_Kb,
        image_order=Image_Order,
        interval=Interval_In_Secs,
        initial_image=Initial_Image_File)
    w.start()
