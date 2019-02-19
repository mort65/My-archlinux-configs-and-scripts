#! /bin/bash
## dwm autostart script

#status toggle
STATUS=2

#kill previous instances of this script
SCRIPT_NAME="autostart.sh"
for pid in $(pidof -x "$SCRIPT_NAME"); do
    if [ "$pid" != $$ ]; then
        kill "$pid" > /dev/null 2>&1
    fi
done
sleep 2s
mapfile -t pids  < <(pgrep "$SCRIPT_NAME" | grep -v $$)
kill -9 "${pids[@]}" > /dev/null 2>&1

sleep 1s

~/.script/dwm-sendsignal 0;
pgrep -c lxpolkit || exec /usr/bin/lxpolkit &
pgrep -c pcmanfm || exec dbus-launch pcmanfm -d &
/usr/bin/numlockx &
/usr/bin//nitrogen --restore &
sleep 1s
pgrep -c gxkb || exec /usr/bin/gxkb &
pgrep -c compton || exec /usr/bin/compton -b &
pgrep -c volumeicon || exec /usr/bin/volumeicon &
pgrep -c udiskie || exec /usr/bin/udiskie -2 -s &
pgrep -c clipit || exec /usr/bin/clipit &
pgrep -c nm-applet || exec /usr/bin/nm-applet &

sleep 1s

if [ $STATUS -eq 1 ]; then
	pkill -c --signal=SIGTERM 'conky|dzen2'
	sleep 1s
	while true; do
		"$HOME/.dwm/status.sh" &> /dev/null
		sleep 10s
	done &
elif [ $STATUS -eq 2 ]; then
	pkill -c --signal=SIGTERM 'conky|dzen2'; sleep 1s ; ~/.script/dwm-status_dzen &
fi

exit 0
