#
# ~/.zprofile
#

export PATH=$PATH:$HOME/bin
export EDITOR="vim"
export TERMINAL="st"
export BROWSER="brave"
export FILEMANAGER="thunar"
export SUDO_ASKPASS="/usr/bin/qt4-ssh-askpass"

if [ "$(tty)" = "/dev/tty1" ]; then
	pgrep "dwm|xfce4-session" || . ~/bin/runx
fi
#if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
#	  exec startx
#fi

