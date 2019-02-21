#!/bin/bash

COOL=65
WARM=80

if [[ $1 < $COOL ]]; then
	echo -e "^fg()$1"    # COOL
elif [[ ! $1 < $WARM ]]; then
	echo -e "^fg(#ff0066)$1"  # HOT
else
	echo -e "^fg(#ffff00)$1"                        # WARM
fi

exit 0
