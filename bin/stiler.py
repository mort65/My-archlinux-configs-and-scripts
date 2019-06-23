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
import socket
import time


def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
        #print 'I got the lock'
    except socket.error:
        #print 'lock exists'
        count = 0.0

        while True:
            time.sleep(0.1)
            try:
                get_lock._lock_socket.bind('\0' + process_name)
                break

            except socket.error:
                count += 0.1
                if count >= 3.0:
                    sys.exit()


get_lock('stiler.py')


def getvalue(value,minvalue,maxvalue):
    if value < minvalue:
        return minvalue

    elif value > maxvalue:
        return maxvalue

    return value


def compare_win_list(newlist,oldlist):
    templist = []
    for window in oldlist:
        if newlist.count(window) != 0:
            templist.append(window)
    for window in newlist:
        if oldlist.count(window) == 0:
            templist.append(window)
    return templist


def compare_win_dict(newdict,olddict):
    if olddict in ({},newdict):
        return newdict

    tempdict = dict()
    for k in newdict.keys():
        if str(k) in olddict:
            tempdict[str(k)] = compare_win_list(newdict[str(k)],olddict[str(k)])
        else:
            tempdict[str[k]] = newdict[str(k)]

    return tempdict


def initialize(id_exclude_set,id_include_set):
    desk_output = commands.getoutput("wmctrl -d").split("\n")
    desk_list = [line.split()[0] for line in desk_output]
    current =  filter(lambda x: x.split()[1] == "*" , desk_output)[0].split()

    desktop = current[0]
    width =   current[8].split("x")[0]
    height =  current[8].split("x")[1]
    orig_x =  current[7].split(",")[0]
    orig_y =  current[7].split(",")[1]

    win_output = commands.getoutput("wmctrl -lGx").split("\n")
    new_win_output = []
    excluded_win_output = []
    idws = [int(win.split()[0],16) for win in win_output]
    new_id_exclude_set = set()
    new_id_include_set = set()

    for idw in id_exclude_set:
        if int(idw,16) in idws:
            new_id_exclude_set.add(idw)

    for idw in id_include_set:
        if int(idw,16) in idws:
            new_id_include_set.add(idw)

    id_exclude_set = [int(idw,16) for idw in new_id_exclude_set]
    id_include_set = [int(idw,16) for idw in new_id_include_set]

    for win in win_output:
        try:
            if int(win.split()[0],16) in id_exclude_set:
                excluded_win_output.append(win)
                continue

            if int(win.split()[0],16) in id_include_set:
                new_win_output.append(win)
                continue

            type_output = commands.getoutput("xprop -id " + win.split()[0] + " _NET_WM_WINDOW_TYPE").split("\n")[0].split(" = ")
            if len(type_output) > 1 and type_output[1] in TypeExcludeList:
                excluded_win_output.append(win)
                continue

            instance_class = win.split()[6]
            if not instance_class:
                new_win_output.append(win)
                continue

            instance_class_list = instance_class.split('.')
            instance_class_list.extend(['',''])
            for exclude in PropExcludeList:
                if exclude[0] and exclude[1]:
                    if (exclude[0] + '.' + exclude[1]) == instance_class:
                        excluded_win_output.append(win)
                        break

                elif exclude[0] or exclude[1]:
                    if (instance_class_list[0] and exclude[0] and instance_class_list[0] == exclude[0]) or \
                    (instance_class_list[1] and exclude[1] and instance_class_list[1] == exclude[1]):
                        excluded_win_output.append(win)
                        break

            else:
                new_win_output.append(win)

        except IndexError:
            new_win_output.append(win)

    win_list = {}
    excluded_win_list = {}

    for desk in desk_list:
        win_list[desk] = map(lambda y: hex(int(y.split()[0],16)) , filter(lambda x: x.split()[1] == desk, new_win_output ))
        excluded_win_list[desk] = map(lambda y: hex(int(y.split()[0],16)) , filter(lambda x: x.split()[1] == desk, excluded_win_output ))

    return (desktop,orig_x,orig_y,width,height,win_list,excluded_win_list,new_id_exclude_set,new_id_include_set)


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

# Global variables

#BottomPadding = 0
#TopPadding = 0
#LeftPadding = 0
#RightPadding = 0
#WinTitle = 21
#WinBorder = 1
#MwFactor = 0.65
#CFactor = 0.75
#TempFile = "/tmp/tile_winlist"
BottomPadding = 0
TopPadding = 0
LeftPadding = 0
RightPadding = 0
WinTitle = 23
WinBorder = 3
OrigMwFactor = 0.5
OrigCFactor = 0.8
TempFile = "/tmp/tile_winlist"
TempFile2 = "/tmp/temp_varlist"
TypeExcludeList = ["_NET_WM_WINDOW_TYPE_DIALOG", "_NET_WM_WINDOW_TYPE_SPLASH", "_NET_WM_WINDOW_TYPE_NOTIFICATION","_NET_WM_WINDOW_TYPE_TOOLBAR"]
PropExcludeList = [("veracrypt","Veracrypt"),("dukto","Dukto"),("nitrogen","Nitrogen"),\
("keepass2","KeePass2"),("galculator","Galculator"),("ultracopier","ultracopier"),\
('',"openssh-askpass"),('',"Wine"),('',"Zenity"),('',"Lutris"),("mlconfig","Mlconfig"),("st","St")]#(instance,class)
OrigMode={"0":"simple","1":"horizontal"}


OldWinList = retrieve(TempFile)
OldVarList = retrieve(TempFile2)
Mode=get_temp_var(OldVarList,0,OrigMode)
MinMwFactor, MaxMwFactor = 0.25, 0.90
MinCFactor, MaxCFactor = 0.3, 1.0
MwFactor=getvalue(get_temp_var(OldVarList,1,OrigMwFactor),MinMwFactor,MaxMwFactor)
CFactor=getvalue(get_temp_var(OldVarList,2,OrigCFactor),MinCFactor,MaxCFactor)
OldIdExcludeSet=get_temp_var(OldVarList,3,set())
OldIdIncludeSet=get_temp_var(OldVarList,4,set())
OldDesktop=get_temp_var(OldVarList,5,set())
(Desktop,OrigXstr,OrigYstr,MaxWidthStr,MaxHeightStr,WinList,ExcludedWinList,IdExcludeSet,IdIncludeSet) = initialize(OldIdExcludeSet,OldIdIncludeSet)
WinList = compare_win_dict(WinList,OldWinList)
MaxWidth = int(MaxWidthStr) - LeftPadding - RightPadding
MaxHeight = int(MaxHeightStr) - TopPadding - BottomPadding
OrigX = int(OrigXstr) + LeftPadding
OrigY = int(OrigYstr) + TopPadding

Reset=False


def store_vars(*args):
    store(args,TempFile2)


def get_simple_tile(wincount):
    rows = wincount - 1
    layout = []
    if rows == 0:
        layout.append((OrigX+WinBorder,OrigY+WinBorder,int(MaxWidth-2*WinBorder),int(MaxHeight-WinTitle-2*WinBorder)))
        return layout

    else:
        layout.append((OrigX+WinBorder,OrigY+WinBorder,int(MaxWidth*MwFactor-2*WinBorder),int(MaxHeight-WinTitle-2*WinBorder)))

    x=OrigX + int((MaxWidth*MwFactor)+WinBorder)
    width=int((MaxWidth*(1-MwFactor))-2*WinBorder)
    height=int(MaxHeight/rows-WinTitle-2*WinBorder)

    for n in range(0,rows):
        y= OrigY+int((MaxHeight/rows)*(n)+WinBorder)
        layout.append((x,y,width,height))

    return layout


def get_vertical_tile(wincount):
    layout = []
    y = OrigY + WinBorder
    width = int(MaxWidth/wincount-2*WinBorder)
    height = int(MaxHeight-WinTitle-2*WinBorder)
    for n in range(0,wincount):
        x= int(OrigX+n*(MaxWidth/wincount)+WinBorder)
        layout.append((x,y,width,height))

    return layout


def get_horiz_tile(wincount):
    layout = []
    x = OrigX+WinBorder
    height = int(MaxHeight/wincount-WinTitle-2*WinBorder)
    width = int(MaxWidth-2*WinBorder)
    for n in range(0,wincount):
        y= OrigY + int((MaxHeight/wincount)*(n)+WinBorder)
        layout.append((x,y,width,height))

    return layout


def get_center_tile(wincount):
    layout = []
    width=int(MaxWidth*CFactor)
    height=int(MaxHeight*CFactor-WinTitle)
    x=int(OrigX+MaxWidth/2-width/2)
    y=int(OrigY+MaxHeight/2-height/2-WinTitle)
    for n in range(0,wincount):
        layout.append((x,y,width,height))

    return layout


def get_left_tile(wincount):
    layout = []
    width=int(MaxWidth*MwFactor)
    height=MaxHeight-WinTitle-WinBorder
    x=OrigX
    y=OrigY
    layout.append((x,y,width,height))

    width=int(MaxWidth*(1-MwFactor))-2*WinBorder
    x=int(MaxWidth*MwFactor)+OrigX+2*WinBorder
    for n in range(0,wincount-1):
        layout.append((x,y,width,height))

    return layout


def get_right_tile(wincount):
    layout = []
    width=int(MaxWidth*(1-MwFactor))-2*WinBorder
    height=MaxHeight-WinTitle-WinBorder
    x=int(MaxWidth*MwFactor)+OrigX+2*WinBorder
    y=OrigY
    layout.append((x,y,width,height))

    width=int(MaxWidth*MwFactor)
    x=OrigX
    for n in range(0,wincount-1):
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
    command =  " wmctrl -r " + windowid +  " -e 0," + str(PosX) + "," + str(PosY)+ "," + str(Width) + "," + str(Height) + " -i"
    os.system(command)
    command = "wmctrl -r " + windowid + " -b remove,hidden,shaded -i"
    os.system(command)

def unmaximize_win(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz"
    else:
        command = "wmctrl -r " + windowid + " -b remove,maximized_vert,maximized_horz -i"

    os.system(command)


def normalize_win(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -r :ACTIVE: -b remove,hidden,shaded"
    else:
        command = "wmctrl -r " + windowid + " -b remove,hidden,shaded -i"

    os.system(command)


def maximize_win(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz"
    else:
        command = "wmctrl -r " + windowid + " -b add,maximized_vert,maximized_horz -i"

    os.system(command)


def toggle_maximize_win(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -r :ACTIVE: -b toggle,maximized_vert,maximized_horz"
    else:
        command = "wmctrl -r " + windowid + " -b toggle,maximized_vert,maximized_horz -i"

    os.system(command)


def raise_window(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -a :ACTIVE: "
    else:
        command = "wmctrl -a " + windowid + " -i"

    os.system(command)


def exclude_win(windowid):
    winlist = create_win_list()
    IdExcludeSet.add(windowid)
    if windowid in IdIncludeSet:
        IdIncludeSet.remove(windowid)
    if windowid in winlist:
        winlist.remove(windowid)
    store_vars(Mode,MwFactor,CFactor,IdExcludeSet,IdIncludeSet,Desktop)
    arrange_mode(winlist,Mode[Desktop])


def include_win(windowid):
    winlist = create_win_list()
    if windowid in IdExcludeSet:
        IdExcludeSet.remove(windowid)
    IdIncludeSet.add(windowid)
    if not windowid in winlist:
        winlist.append(windowid)
    store_vars(Mode,MwFactor,CFactor,IdExcludeSet,IdIncludeSet,Desktop)
    arrange_mode(winlist,Mode[Desktop])

def toggle_exclude_win(windowid):
    winlist = create_win_list()
    if windowid in IdIncludeSet:
            IdIncludeSet.remove(windowid)
            IdExcludeSet.add(windowid)
            if windowid in winlist:
                winlist.remove(windowid)
    else:
        IdIncludeSet.add(windowid)
        if windowid in IdExcludeSet:
            IdExcludeSet.remove(windowid)
        if not windowid in winlist:
            winlist.append(windowid)

    store_vars(Mode,MwFactor,CFactor,IdExcludeSet,IdIncludeSet,Desktop)
    arrange_mode(winlist,Mode[Desktop])


def left():
    winlist = create_win_list()
    arrange_mode(winlist,"left")


def right():
    winlist = create_win_list()
    arrange_mode(winlist,"right")


def center():
    winlist = create_win_list()
    active = get_active_window()
    if active in winlist:
        winlist.remove(active)
        winlist.insert(0,active)

    arrange_mode(winlist,"center")


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


def ischanged():
    if not Desktop == OldDesktop:
        return True

    if OldWinList == {}:
        return True

    OldWindows = OldWinList[Desktop]
    Windows = WinList[Desktop]
    if Windows == OldWindows:
        return False

    for window in OldWindows:
        if Windows.count(window) == 0:
            return True

    for window in Windows:
        if OldWindows.count(window) == 0:
            return True

    return False


def arrange(layout,windows):
    for win , lay  in zip(windows,layout):
        move_window(win,lay[0],lay[1],lay[2],lay[3])
    WinList[Desktop]=windows
    store(WinList,TempFile)

def unmaximize_wins(winlist):
    for win in winlist:
        unmaximize_win(win)

def maximize_wins(winlist):
    for win in winlist:
        maximize_win(win)


def normalize_wins(winlist):
    for win in winlist:
        normalize_win(win)


def raise_wins(winlist):
    for win in winlist:
        raise_window(win)


def arrange_mode(wins,mode):

    if Reset:
        unmaximize_wins(WinList[Desktop])
        normalize_wins(WinList[Desktop])
        raise_wins(WinList[Desktop])
        raise_window(WinList[Desktop][0])
    if len(wins) == 0:
        return

    if mode == "simple":
        arrange(get_simple_tile(len(wins)),wins)

    elif mode == "horizontal":
        arrange(get_horiz_tile(len(wins)),wins)

    elif mode == "vertical":
        arrange(get_vertical_tile(len(wins)),wins)

    elif mode == "max_all":
        arrange(get_max_all(len(wins)),wins)

    elif mode == "center":
        arrange(get_center_tile(len(wins)),wins)

    elif mode == "left":
        arrange(get_left_tile(len(wins)),wins)

    elif mode == "right":
        arrange(get_right_tile(len(wins)),wins)

    else:
        arrange(get_simple_tile(len(wins)),wins)

    if Reset:
        raise_wins(ExcludedWinList[Desktop])


def simple():
    Windows = create_win_list()
    arrange_mode(Windows,"simple")


def swap():
    winlist = create_win_list()
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0,active)
    arrange_mode(winlist,Mode[Desktop])


def vertical():
    winlist = create_win_list()
    arrange_mode(winlist,"vertical")


def horiz():
    winlist = create_win_list()
    arrange_mode(winlist,"horizontal")


def cycle(n):
    winlist = create_win_list()
    #n = n % len(winlist)
    winlist = winlist[-n:] + winlist[:-n]
    arrange_mode(winlist,Mode[Desktop])
    raise_window(winlist[0])


def maximize():
    maximize_win(":ACTIVE:")
    raise_window(":ACTIVE:")

def toggle_maximize():
    toggle_maximize_win(":ACTIVE:")
    raise_window(":ACTIVE:")

def max_all():
    winlist = create_win_list()
    active = get_active_window()
    if active in winlist:
        winlist.remove(active)
        winlist.insert(0,active)
    #arrange_mode(winlist,"max_all")
    maximize_wins(winlist)
    raise_window(winlist[0])


def setmwfactor(mf):
    mf = getvalue(mf,MinMwFactor,MaxMwFactor)
    store_vars(Mode,mf,CFactor,IdExcludeSet,IdIncludeSet,Desktop)

    return mf


def setcfactor(cf):
    cf = getvalue(cf,MinCFactor,MaxCFactor)
    store_vars(Mode,MwFactor,cf,IdExcludeSet,IdIncludeSet,Desktop)

    return cf

def normalize():
    set_mode(Mode[Desktop])

def unmaximize():
    unmaximize_win(":ACTIVE:")
    raise_window(":ACTIVE:")


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
    elif mode == "left":
        left()
    elif mode == "right":
        right()
    else:
        return

    Mode[Desktop] = mode

    store_vars(Mode,MwFactor,CFactor,IdExcludeSet,IdIncludeSet,Desktop)


if len(sys.argv) < 2 or sys.argv[1] in ("", "-h","--help"):
    print("""\
Usage: styler.py [OPTION]
Options:
         simple,horizontal,vertical,max_all,center,left,right,
         maximize,unmaximize,normalize,toggle_maximize
         inc_mwfactor,dec_mwfactor,reset_mwfactor,
         inc_cfactor,dec_cfactor,reset_cfactor,
         exclude,include,toggle_exclude,
         swap,cycle,reverse_cycle,
         reset,daemon\
         """)
    sys.exit()
elif sys.argv[1] == "reset":
    Reset = True
    set_mode(Mode[Desktop])
elif sys.argv[1] == "daemon":
    if ischanged():
        set_mode(Mode[Desktop])
elif sys.argv[1] in ("simple", "horizontal", "vertical", "max_all", "center", "left", "right"):
    Reset = True
    Mode[Desktop] = sys.argv[1]
    set_mode(sys.argv[1])
elif sys.argv[1] == "swap":
    swap()
elif sys.argv[1] == "cycle":
    cycle(1)
elif sys.argv[1] == "reverse_cycle":
    cycle(-1)
elif sys.argv[1] == "maximize":
    maximize()
elif sys.argv[1] == "toggle_maximize":
    toggle_maximize()
elif sys.argv[1] == "unmaximize":
    unmaximize()
elif sys.argv[1] == "normalize":
    Reset = True
    normalize()
elif sys.argv[1] == "exclude":
    active = get_active_window()
    if active:
        exclude_win(active)
elif sys.argv[1] == "include":
    active = get_active_window()
    if active:
        include_win(active)
elif sys.argv[1] == "toggle_exclude":
    active = get_active_window()
    if active:
        toggle_exclude_win(active)
elif sys.argv[1] == "inc_mwfactor":
    Reset = True
    MwFactor=setmwfactor(MwFactor+0.05)
    if Mode[Desktop] in ("simple", "left", "right"):
        set_mode(Mode[Desktop])
    else:
        set_mode("simple")
elif sys.argv[1] == "dec_mwfactor":
    Reset = True
    MwFactor=setmwfactor(MwFactor-0.05)
    if Mode[Desktop] in ("simple", "left", "right"):
        set_mode(Mode[Desktop])
    else:
        set_mode("simple")
elif sys.argv[1] == "reset_mwfactor":
    Reset = True
    MwFactor=setmwfactor(OrigMwFactor)
    if Mode[Desktop] in ("simple", "left", "right"):
        set_mode(Mode[Desktop])
    else:
        set_mode("simple")
elif sys.argv[1] == "dec_cfactor":
    Reset = True
    CFactor=setcfactor(CFactor-0.05)
    set_mode("center")
elif sys.argv[1] == "inc_cfactor":
    Reset = True
    CFactor=setcfactor(CFactor+0.05)
    set_mode("center")
elif sys.argv[1] == "reset_cfactor":
    Reset = True
    CFactor=setcfactor(OrigCFactor)
    set_mode("center")


