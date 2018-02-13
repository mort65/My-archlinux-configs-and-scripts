#!/usr/bin/env python3

import os
import glob
import random

cows = [ os.path.basename(cow)
for cow in glob.glob("/usr/share/cows/*.cow") ]
c=cows[random.randint(0,len(cows)-1)]
i=random.randint(1,6)
cmds = ["/usr/bin/cowsay -f {}".format(c),
"/usr/bin/cowthink -f {}".format(c),
"/usr/bin/ponysay --colour '1;3{}'".format(i),
"/usr/bin/ponythink --colour '1;3{}'".format(i)]
os.system("/usr/bin/fortune -a | {}".format(cmds[random.randint(0,len(cmds)-1)]))
