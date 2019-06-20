#!/usr/bin/python2

############################################################################
# Copyright (c) 2009   unohu <unohu0@gmail.com>                            #
#                                                                          #
# Permission to use, copy, modify, and/or distribute this software for any #
# purpose with or without fee is hereby granted, provided that the above   #
# copyright notice and this permission notice appear in all copies.        #
#                                                                          #
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES #
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF         #
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR  #
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES   #
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN    #
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF  #
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.           #
#                                                                          #
############################################################################

import sys
import os
import commands
import pickle
import ConfigParser

def initconfig():
    rcfile=os.getenv('HOME')+"/.stilerrc"
    if not os.path.exists(rcfile):
        cfg=open(rcfile,'w')
        cfg.write("""#Tweak these values
[default]
BottomPadding = 0
TopPadding = 0
LeftPadding = 0
RightPadding = 0
WinTitle = 21
WinBorder = 1
MwFactor = 0.65
CFactor = 0.75
TempFile = /tmp/tile_winlist
TempFile2 = /tmp/temp_varlist
""")
        cfg.close()

    config=ConfigParser.RawConfigParser()
    config.read(rcfile)
    return config

def getvalue(value,minvalue,maxvalue):
    if value < minvalue:
        return minvalue
    elif value > maxvalue:
        return maxvalue
    return value
    
def initialize():
    desk_output = commands.getoutput("wmctrl -d").split("\n")
    desk_list = [line.split()[0] for line in desk_output]
    current =  filter(lambda x: x.split()[1] == "*" , desk_output)[0].split()

    desktop = current[0]
    width =   current[8].split("x")[0]
    height =  current[8].split("x")[1]
    orig_x =  current[7].split(",")[0]
    orig_y =  current[7].split(",")[1]

    win_output = commands.getoutput("wmctrl -lG").split("\n")
    win_list = {}

    for desk in desk_list:
        win_list[desk] = map(lambda y: hex(int(y.split()[0],16)) , filter(lambda x: x.split()[1] == desk, win_output ))

    return (desktop,orig_x,orig_y,width,height,win_list)

def get_active_window():
    return str(hex(int(commands.getoutput("xdotool getactivewindow 2>/dev/null").split()[0])))


def store(object,file):
    with open(file, 'w') as f:
        pickle.dump(object,f)
    f.close()


def retrieve(file):
    try:
        with open(file,'r+') as f:
            obj = pickle.load(f)
        f.close()
        return(obj)
    except:
        f = open(file,'w')
        f.close
        dict = {}
        return (dict)

    
def get_temp_var(var_list,index,def_value):
    if var_list == {}:
        return def_value
    return var_list[index]

# Get all global variables
Config = initconfig()
BottomPadding = Config.getint("default","BottomPadding")
TopPadding = Config.getint("default","TopPadding")
LeftPadding = Config.getint("default","LeftPadding")
RightPadding = Config.getint("default","RightPadding")
WinTitle = Config.getint("default","WinTitle")
WinBorder = Config.getint("default","WinBorder")
OrigMwFactor = Config.getfloat("default","MwFactor")
OrigCFactor = Config.getfloat("default","CFactor")
TempFile = Config.get("default","TempFile")
TempFile2 = Config.get("default","TempFile2")
(Desktop,OrigXstr,OrigYstr,MaxWidthStr,MaxHeightStr,WinList) = initialize()
MaxWidth = int(MaxWidthStr) - LeftPadding - RightPadding
MaxHeight = int(MaxHeightStr) - TopPadding - BottomPadding
OrigX = int(OrigXstr) + LeftPadding
OrigY = int(OrigYstr) + TopPadding
OldWinList = retrieve(TempFile)
OldVarList = retrieve(TempFile2)
Mode=get_temp_var(OldVarList,0,"Simple")
MinMwFactor, MaxMwFactor = 0.25, 0.90
MinCFactor, MaxCFactor = 0.3, 1.0
MwFactor=getvalue(get_temp_var(OldVarList,1,OrigMwFactor),MinMwFactor,MaxMwFactor)
CFactor=getvalue(get_temp_var(OldVarList,2,OrigCFactor),MinCFactor,MaxCFactor)


def store_vars(*args):
    store(args,TempFile2)


def get_simple_tile(wincount):
    rows = wincount - 1
    layout = []
    if rows == 0:
        layout.append((OrigX,OrigY,MaxWidth,MaxHeight-WinTitle-WinBorder))
        return layout
    else:
        layout.append((OrigX,OrigY,int(MaxWidth*MwFactor),MaxHeight-WinTitle-WinBorder))

    x=OrigX + int((MaxWidth*MwFactor)+(2*WinBorder))
    width=int((MaxWidth*(1-MwFactor))-2*WinBorder)
    height=int(MaxHeight/rows-WinTitle-WinBorder)

    for n in range(0,rows):
        y= OrigY+int((MaxHeight/rows)*(n))
        layout.append((x,y,width,height))

    return layout


def get_vertical_tile(wincount):
    layout = []
    y = OrigY
    width = int(MaxWidth/wincount)
    height = MaxHeight - WinTitle - WinBorder
    for n in range(0,wincount):
        x= OrigX + n * width
        layout.append((x,y,width,height))

    return layout


def get_horiz_tile(wincount):
    layout = []
    x = OrigX
    height = int(MaxHeight/wincount - WinTitle - WinBorder)
    width = MaxWidth
    for n in range(0,wincount):
        y= OrigY + int((MaxHeight/wincount)*(n))
        layout.append((x,y,width,height))

    return layout
    
def get_center_tile(wincount):
    layout = []
    width=int(MaxWidth*CFactor)
    height=int(MaxHeight*CFactor)-WinTitle
    x=int(MaxWidth/2)+OrigX-int(width/2)
    y=int(MaxHeight/2)+OrigY-int(height/2)-WinTitle
    for n in range(0,wincount):
        layout.append((x,y,width,height))

    return layout


def get_max_all(wincount):
    layout = []
    x = OrigX
    y = OrigY
    height = MaxHeight - WinTitle - WinBorder
    width = MaxWidth
    for n in range(0,wincount):
        layout.append((x,y,width,height))

    return layout


def move_active(PosX,PosY,Width,Height):
    command =  " wmctrl -r :ACTIVE: -e 0," + str(PosX) + "," + str(PosY)+ "," + str(Width) + "," + str(Height)
    os.system(command)


def move_window(windowid,PosX,PosY,Width,Height):
    command =  " wmctrl -i -r " + windowid +  " -e 0," + str(PosX) + "," + str(PosY)+ "," + str(Width) + "," + str(Height)
    os.system(command)
    command = "wmctrl -i -r " + windowid + " -b remove,hidden,shaded"
    os.system(command)


def raise_window(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -a :ACTIVE: "
    else:
        command = "wmctrl -i -a " + windowid

    os.system(command)


def left():
    Width=int(MaxWidth*MwFactor)
    Height=MaxHeight-WinTitle-WinBorder
    PosX=OrigX
    PosY=OrigY
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")


def right():
    Width=int(MaxWidth*(1-MwFactor))-2*WinBorder
    Height=MaxHeight-WinTitle-WinBorder
    PosX=int(MaxWidth*MwFactor)+OrigX+2*WinBorder
    PosY=OrigY
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")


def center():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange(get_center_tile(len(winlist)),winlist)
    

def compare_win_list(newlist,oldlist):
    templist = []
    for window in oldlist:
        if newlist.count(window) != 0:
            templist.append(window)
    for window in newlist:
        if oldlist.count(window) == 0:
            templist.append(window)
    return templist


def create_win_list():
    Windows = WinList[Desktop]

    if OldWinList == {}:
        pass
    else:
        OldWindows = OldWinList[Desktop]
        if Windows == OldWindows:
            pass
        else:
            Windows = compare_win_list(Windows,OldWindows)

    return Windows


def arrange(layout,windows):
    for win , lay  in zip(windows,layout):
        move_window(win,lay[0],lay[1],lay[2],lay[3])
    WinList[Desktop]=windows
    store(WinList,TempFile)


def arrange_mode(wins):
    if Mode == "simple":
        arrange(get_simple_tile(len(wins)),wins)
    elif Mode == "horizontal":
        arrange(get_horiz_tile(len(wins)),wins)
    elif Mode == "vertical":
        arrange(get_vertical_tile(len(wins)),wins)
    elif Mode == "max_all":
        arrange(get_max_all(len(wins)),wins)
    elif Mode == "center":
        arrange(get_center_tile(len(wins)),wins)
    else:
        arrange(get_simple_tile(len(wins)),wins)


def simple():
    Windows = create_win_list()
    arrange(get_simple_tile(len(Windows)),Windows)


def swap():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange_mode(winlist)


def vertical():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange(get_vertical_tile(len(winlist)),winlist)


def horiz():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange(get_horiz_tile(len(winlist)),winlist)


def cycle():
    winlist = create_win_list()
    winlist.insert(0,winlist[len(winlist)-1])
    winlist = winlist[:-1]
    arrange_mode(winlist)
    raise_window(winlist[0])


def maximize():
    Width=MaxWidth
    Height=MaxHeight-WinTitle-WinBorder
    PosX=OrigX
    PosY=OrigY
    move_active(PosX,PosY,Width,Height)
    raise_window(":ACTIVE:")

def max_all():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange(get_max_all(len(winlist)),winlist)

  
def setmwfactor(mf):
    mf = getvalue(mf,MinMwFactor,MaxMwFactor)
    store_vars(Mode,mf,CFactor)
    
    return mf


def setcfactor(cf):
    cf = getvalue(cf,MinCFactor,MaxCFactor)
    store_vars(Mode,MwFactor,cf)
    
    return cf
    

def set_mode(mode):
    if mode == "simple":
        simple()
    elif mode == "horizontal":
        horiz()
    elif mode == "vertical":
        vertical()
    elif mode == "max_all":
        max_all()
    elif mode == "center":
        center()
    else:
        return
    
    store_vars(mode,MwFactor,CFactor)

       
if len(sys.argv) < 2:
    set_mode(Mode)
elif sys.argv[1] in ("simple", "horizontal", "vertical", "max_all", "center"):
    set_mode(sys.argv[1])
elif sys.argv[1] == "left":
    left()
elif sys.argv[1] == "right":
    right()
elif sys.argv[1] == "swap":
    swap()
elif sys.argv[1] == "cycle":
    cycle()
elif sys.argv[1] == "maximize":
    maximize()
elif sys.argv[1] == "inc_mwfactor":
    MwFactor=setmwfactor(MwFactor+0.05)
    set_mode("simple")
elif sys.argv[1] == "dec_mwfactor":
    MwFactor=setmwfactor(MwFactor-0.05)
    set_mode("simple")
elif sys.argv[1] == "reset_mwfactor":
    MwFactor=setmwfactor(OrigMwFactor)
    set_mode("simple")
elif sys.argv[1] == "dec_cfactor":
    CFactor=setcfactor(CFactor-0.05)
    set_mode("center")
elif sys.argv[1] == "inc_cfactor":
    CFactor=setcfactor(CFactor+0.05)
    set_mode("center")
elif sys.argv[1] == "reset_cfactor":
    CFactor=setcfactor(OrigCFactor)
    set_mode("center")


