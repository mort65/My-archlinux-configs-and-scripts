#! /bin/bash
## my dwm status script

CDATE () {
	cdate=$(/usr/bin/date +"%a %b %d %H:%M")
	echo "${cdate}"
}

CTIME () {
	ctime=$(/usr/bin/jdate +"%h %H:%M")
	echo "${ctime}"
}

CTEMP () {
	ctemp=$("$HOME/bin/ctemp" --max)
	echo "${ctemp}"
}

GTEMP () {
	gtemp=$("$HOME/bin/gtemp")
	echo "${gtemp}"
}

/usr/bin/xsetroot -name "  [$(CTEMP) $(GTEMP)]   [$(CDATE)] "
#/usr/bin/xsetroot -name "[$(CDATE)]"

