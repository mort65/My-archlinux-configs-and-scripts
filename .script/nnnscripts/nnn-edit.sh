#!/usr/bin/env sh
# Description: Fuzzy find a file in directory subtree with fzy and edit in vim

vim $(find -type f | fzy) 2>&1

