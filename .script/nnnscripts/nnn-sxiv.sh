#!/usr/bin/env sh
# Description: Open images in current directory in sxiv

sxiv -q $(tree --noreport -ifax) >/dev/null 2>&1 &
