#! /bin/bash
## dwm autostart script

sleep 1s

#kill previous instances of this script
/usr/bin/pgrep autostart.sh | /usr/bin/tac | /usr/bin/awk 'NR > 1' | /usr/bin/xargs kill -9 &> /dev/null

#status toggle
STATUS=2

sleep 1s
dwm-clearstatus
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
