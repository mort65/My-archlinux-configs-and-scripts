#!/usr/bin/env sh
#sets the selected picture in nnn as wallpaper

FILE="$(< ~/.nnncp tr '\0' '\n' | grep -iE '\.png$|\.bmp$|\.jpe?g$' | tail -1)"
[ -n "${FILE}" ] && nitrogen --save --set-scaled "${FILE}"
