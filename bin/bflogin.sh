#!/bin/bash
#fix for dark theme on kde apps
BKFILE=~/.gtkrc-2.0.bk 
ORGFILE=~/.gtkrc-2.0
if [[ "$XDG_CURRENT_DESKTOP" == "MATE" ]]; then
    if [ -f $ORGFILE ]; then
        /usr/bin/mv -f $ORGFILE $BKFILE
    fi
else
	if [ -f $BKFILE ]; then
		/usr/bin/mv -f $BKFILE $ORGFILE
	fi
fi
