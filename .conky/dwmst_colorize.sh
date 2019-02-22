#!/bin/bash

COOL=65
WARM=80
NUM="$(echo "$1" | tr -dc '0-9.\n')"

if (( $(bc -l<<<"$NUM<$COOL") )); then
	echo -e "^fg()$1"    # COOL
elif (( $(bc -l<<<"$NUM>=$WARM") )); then
	echo -e "^fg(#ff0066)$1"  # HOT
else
	echo -e "^fg(#ffff00)$1"                        # WARM
fi

exit 0
