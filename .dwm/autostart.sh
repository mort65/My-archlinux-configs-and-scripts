#! /bin/bash
## dwm autostart script

#status toggle
STATUS=0

pgrep -c lxpolkit || /usr/bin/lxpolkit &
pgrep -c pcmanfm || dbus-launch pcmanfm -d &
/usr/bin/numlockx &
/usr/bin//nitrogen --restore &
sleep 1
pgrep -c gxkb || /usr/bin/gxkb &
pgrep -c compton || /usr/bin/compton -b &
pgrep -c volumeicon || /usr/bin/volumeicon &
pgrep -c udiskie || /usr/bin/udiskie -2 -s &
pgrep -c clipit || /usr/bin/clipit &
pgrep -c nm-applet || /usr/bin/nm-applet &
sleep 1
pkill -c --signal=SIGTERM 'conky|dzen2'; sleep 1s ; ~/.script/dwm-status_dzen &


if [ $STATUS -eq 1 ]; then
	while true; do
		"$HOME/.dwm/status.sh" &> /dev/null
		sleep 10s
	done &
else
	sleep 1s;
	~/.script/dwm-sendsignal 0;

fi
