#!/usr/bin/env sh
#play the selected file with mpv and load all subs in the directory

FILE="$(< ~/.nnncp tr '\0' '\n' | tail -1)"
[ -n "${FILE}" ] && mpv "${FILE}" --sub-auto=all
