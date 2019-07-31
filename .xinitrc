#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
	xrdb -merge $sysresources
fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then
	xrdb -merge "$userresources"
fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

# start some nice programs

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

/usr/bin/systemctl --user import-environment DISPLAY

# Here dwm is kept as default
session=${1:-dwm}

killall xbindkeys

case $session in
    dwm               )
	    export DESKTOP_SESSION="dwm"
	    echo 'dwm' > ~/.session
	    exec dwm
	    ;;
    xfce|xfce4        )
	    export DESKTOP_SESSION="xfce4"
	    echo 'xfce4' > ~/.session
	    exec startxfce4
	    ;;
    lxqt              )
	    xbindkeys -f ~/.xbindkeysrc-lxqt
	    export DESKTOP_SESSION="lxqt"
	    echo 'lxqt' > ~/.session
	    exec startlxqt
	    ;;
    openbox           )
	    export DESKTOP_SESSION="openbox"
	    echo 'openbox' > ~/.session
	    exec openbox-session
	    ;;
    # No known session, try to run it as command
    *                 ) exec "$1";;
esac

