#!/bin/bash

# Set keyboard layouts
exec /usr/bin/setxkbmap us,ir -option 'grp:alt_shift_toggle' &

exec /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# Start compositor
exec /usr/bin/compton &

# Start network manager applet
exec /usr/bin/nm-applet &

# Start volume icon for pulseaudio
exec /usr/bin/volumeicon &

exec /usr/bin/clipit &
exec /usr/bin/indicator-kdeconnect &
exec /usr/bin/udiskie -2 -s &
exec ~/bin/enablenotifyforcronie &
exec ~/bin/logupdates &

# Set desktop wallpaper
exec ~/bin/change-desktop-wallpaper.py &

#replace mate notification daemon with xfce notification daemon:
killall mate-notification-daemon &> /dev/null
exec /usr/lib/xfce4/notifyd/xfce4-notifyd &
