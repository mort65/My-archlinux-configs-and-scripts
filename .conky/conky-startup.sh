#!/bin/sh
USERNAME=${SUDO_USER:-$(id -u -n)}
HOMEDIR="/home/$USERNAME"
sleep 20s
killall conky
cd "HOMEDIR/.conky/Gotham3"
conky -c "HOMEDIR/.conky/Gotham3/Gotham3" &
