#!/usr/bin/env sh
# Description: Copy selection to clipboard

cat ~/.nnncp | xargs -0 | xsel -bi
