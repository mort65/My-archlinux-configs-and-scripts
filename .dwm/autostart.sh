#! /bin/bash
## dwm autostart script

#status toggle
STATUS=2

~/.script/dwm-sendsignal 0;
pgrep -c lxpolkit || /usr/bin/lxpolkit &
pgrep -c pcmanfm || dbus-launch pcmanfm -d &
/usr/bin/numlockx &
/usr/bin//nitrogen --restore &
sleep 1s
pgrep -c gxkb || /usr/bin/gxkb &
pgrep -c compton || /usr/bin/compton -b &
pgrep -c volumeicon || /usr/bin/volumeicon &
pgrep -c udiskie || /usr/bin/udiskie -2 -s &
pgrep -c clipit || /usr/bin/clipit &
pgrep -c nm-applet || /usr/bin/nm-applet &

sleep 1s

#kill previous instances of this script
kill $(pgrep autostart.sh | grep -v $$)

sleep 2s

if [ $STATUS -eq 1s ]; then
	pkill -c --signal=SIGTERM 'conky|dzen2'
	sleep 1s
	while true; do
		"$HOME/.dwm/status.sh" &> /dev/null
		sleep 10s
	done &
elif [ $STATUS -eq 2 ]; then
	pkill -c --signal=SIGTERM 'conky|dzen2'; sleep 1s ; ~/.script/dwm-status_dzen &
fi
