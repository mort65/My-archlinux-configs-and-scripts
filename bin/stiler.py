#!/usr/bin/python3
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
import subprocess
import pickle
import socket
import time

# Global variables
##############################
# BottomPadding = 0
# TopPadding = 0
# LeftPadding = 0
# RightPadding = 0
# WinTitle = 21
# WinBorder = 1
# MwFactor = 0.65
# CFactor = 0.75
# TempFile = "/tmp/tile_winlist"
BottomPadding = 0
TopPadding = -2
LeftPadding = -2
RightPadding = 0
WinTitle = 23
WinBorder = 3
OrigMwFactor = 0.5
OrigCFactor = 0.8
MinMwFactor, MaxMwFactor = 0.25, 0.90
MinCFactor, MaxCFactor = 0.3, 1.0
TempFile = "/tmp/tile_winlist"
TempFile2 = "/tmp/temp_varlist"
StateExcludeList = [
    "_NET_WM_STATE_HIDDEN",
    "_NET_WM_STATE_STICKY",
    "_NET_WM_STATE_MODAL",
]
ActionIncludeList = ["_NET_WM_ACTION_RESIZE", "_NET_WM_ACTION_MOVE"]
TypeExcludeList = [
    "_NET_WM_WINDOW_TYPE_DIALOG",
    "_NET_WM_WINDOW_TYPE_SPLASH",
    "_NET_WM_WINDOW_TYPE_TOOLBAR",
    "_NET_WM_WINDOW_TYPE_NOTIFICATION",
]
# (instance,class,"win properties to add")
PropExcludeList = [
    ("", "Wine", ""),
    ("", "Lutris", ""),
    ("", "mpv", "above"),
    ("st", "St", "above"),
    ("totem", "Totem", ""),
    ("", "Zenity", "above"),
    ("", "Tor Browser", ""),
    ("dukto", "Dukto", "above"),
    ("", "Send Anywhere", "above"),
    ("feedreader", "Feedreader", ""),
    ("", "openssh-askpass", "above"),
    ("nitrogen", "Nitrogen", "above"),
    ("keepass2", "KeePass2", "above"),
    ("mlconfig", "Mlconfig", "above"),
    ("veracrypt", "Veracrypt", "above"),
    ("galculator", "Galculator", "above"),
    ("ultracopier", "ultracopier", "above"),
    ("gcr-prompter", "Gcr-prompter", "above"),
    ("brave-browser", "Brave-browser", "maximized_vert,maximized_horz"),
]
OrigMode = {"0": "simple", "1": "horiz"}
##############################


def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        get_lock._lock_socket.bind("\0" + process_name)
        # print('I got the lock')
    except socket.error:
        # print('lock exists')
        count = 0.0
        while True:
            time.sleep(0.1)
            try:
                get_lock._lock_socket.bind("\0" + process_name)
                break
            except socket.error:
                count += 0.1
                if count >= 3.0:
                    sys.exit(1)


get_lock("stiler.py")


def getvalue(value, minvalue, maxvalue):
    if value < minvalue:
        return minvalue
    elif value > maxvalue:
        return maxvalue
    return value


def compare_win_list(newlist, oldlist):
    templist = []
    for window in oldlist:
        if newlist.count(window) != 0:
            templist.append(window)
    for window in newlist:
        if oldlist.count(window) == 0:
            templist.append(window)
    return templist


def compare_win_dict(newdict, olddict):
    if olddict in ({}, newdict):
        return newdict
    tempdict = dict()
    for k in list(newdict.keys()):
        k = str(k)
        if k in olddict:
            tempdict[k] = compare_win_list(newdict[k], olddict[k])
        else:
            tempdict[k] = newdict[k]
    return tempdict


def win_prop(windowid, prop):
    try:
        return subprocess.getoutput(
            "xprop -notype -id " + windowid + " " + prop
        ).split(" = ")[1]
    except BaseException:
        return ""


def win_props(windowid, props):
    try:
        Result = []
        output = subprocess.getoutput(
            "xprop -notype -id " + windowid + " " + " ".join(props)
        ).split("\n")
        for index in range(len(output)):
            if index == len(props):
                break
            if output[index]:
                try:
                    Result.append(output[index].split(" = ")[1])
                except IndexError:
                    Result.append("")
            else:
                Result.append("")
        return Result
    except BaseException:
        return ["" for i in range(len(props))]


def is_type_excluded(windowtype):
    return windowtype in TypeExcludeList if windowtype else False


def is_actions_included(windowactions):
    return (
        set(ActionIncludeList).issubset(windowactions.split(", "))
        if windowactions
        else False
    )


def is_state_excluded(windowstate):
    return (
        not set(StateExcludeList).isdisjoint(windowstate.split(", "))
        if windowstate
        else False
    )


def is_class_excluded(winclass):
    index = 0
    for exclude in PropExcludeList:
        if (not exclude[0] or (exclude[0] == winclass[0])) and (
            not exclude[1] or (exclude[1] == winclass[1])
        ):
            return index
        index += 1
    return -1


def get_win_props(windowid):
    win_type = ""
    win_state = ""
    win_actions = ""
    win_class = ["", ""]
    winprops = win_props(
        windowid,
        (
            "WM_CLASS",
            "_NET_WM_WINDOW_TYPE",
            "_NET_WM_STATE",
            "_NET_WM_ALLOWED_ACTIONS",
        ),
    )
    if winprops:
        if winprops[0]:
            win_class = [s.strip('"') for s in winprops[0].split(", ")]
            if len(win_class) == 1:
                win_class.append("")
        if len(winprops) > 1:
            win_type = winprops[1]
        if len(winprops) > 2:
            win_state = winprops[2]
        if len(winprops) > 3:
            win_actions = winprops[3]
    return (win_class, win_type, win_state, win_actions)


def is_includible(dec_wid, id_include_set, win_type, win_state, win_actions):
    return not (
        is_state_excluded(win_state)
        or not is_actions_included(win_actions)
        or dec_wid not in id_include_set
        and is_type_excluded(win_type)
    )


def set_win_props(windowid, props):
    if props:
        os.system("wmctrl -r " + windowid + " -b add," + props + " -i")


def initialize(id_exclude_set, id_include_set):
    desk_output = subprocess.getoutput("wmctrl -d").split("\n")
    desk_list = [line.split()[0] for line in desk_output]
    current = [x for x in desk_output if x.split()[1] == "*"][0].split()
    desktop = current[0]
    width = current[8].split("x")[0]
    height = current[8].split("x")[1]
    orig_x = current[7].split(",")[0]
    orig_y = current[7].split(",")[1]
    win_output = subprocess.getoutput("wmctrl -l").split("\n")
    new_win_output = []
    excluded_win_output = []
    idws = [int(win.split()[0], 16) for win in win_output]
    new_id_exclude_set = set()
    new_id_include_set = set()
    for idw in id_exclude_set:
        if int(idw, 16) in idws:
            new_id_exclude_set.add(idw)
    for idw in id_include_set:
        if int(idw, 16) in idws:
            new_id_include_set.add(idw)
    id_exclude_set = [int(idw, 16) for idw in new_id_exclude_set]
    id_include_set = [int(idw, 16) for idw in new_id_include_set]
    prop_excluded_list = []
    for win in win_output:
        try:
            wid = win.split()[0]
            dec_wid = int(wid, 16)
            win_desk = win.split()[1]
            if win_desk != desktop:
                new_win_output.append(win)
                continue
            (win_class, win_type, win_state, win_actions) = get_win_props(wid)
            if not is_includible(
                dec_wid, id_include_set, win_type, win_state, win_actions
            ):
                if win_class:
                    index = is_class_excluded(win_class)
                    if index > -1:
                        if dec_wid not in id_exclude_set:
                            id_exclude_set.append(dec_wid)
                        prop_excluded_list.append((wid, index))
                excluded_win_output.append(win)
                continue
            if len(win_class) != 2:
                new_win_output.append(win)
                continue
            if dec_wid in id_exclude_set:
                excluded_win_output.append(win)
                index = is_class_excluded(win_class)
                if index > -1:
                    prop_excluded_list.append((wid, index))
                continue
            if dec_wid in id_include_set:
                new_win_output.append(win)
                continue
            if not win_class[0] + win_class[1]:
                new_win_output.append(win)
                continue
            index = is_class_excluded(win_class)
            if index > -1:
                if dec_wid not in id_exclude_set:
                    id_exclude_set.append(dec_wid)
                excluded_win_output.append(win)
                prop_excluded_list.append((wid, index))
                continue
            new_win_output.append(win)
        except IndexError:
            new_win_output.append(win)
    new_id_exclude_set = set([hex(idw) for idw in id_exclude_set])
    new_id_include_set = set([hex(idw) for idw in id_include_set])
    win_list = {}
    actual_win_list = {}
    excluded_win_list = {}
    for desk in desk_list:
        win_list[desk] = [
            hex(int(y.split()[0], 16))
            for y in [x for x in new_win_output if x.split()[1] == desk]
        ]
        actual_win_list[desk] = [
            hex(int(y.split()[0], 16))
            for y in [x for x in win_output if x.split()[1] == desk]
        ]
        excluded_win_list[desk] = [
            hex(int(y.split()[0], 16))
            for y in [x for x in excluded_win_output if x.split()[1] == desk]
        ]
    return (
        desktop,
        orig_x,
        orig_y,
        width,
        height,
        actual_win_list,
        win_list,
        excluded_win_list,
        new_id_exclude_set,
        new_id_include_set,
        prop_excluded_list,
    )


def get_active_window():
    return str(
        hex(
            int(
                subprocess.getoutput(
                    "xdotool getactivewindow 2>/dev/null"
                ).split()[0]
            )
        )
    )


def store(obj, fname):
    with open(fname, "wb") as f:
        pickle.dump(obj, f)
    f.close()


def retrieve(fname):
    try:
        with open(fname, "rb+") as f:
            obj = pickle.load(f)
        f.close()
        return obj
    except BaseException:
        with open(fname, "wb"):
            pass
        return {}


def get_temp_var(var_list, index, def_value):
    if len(var_list) < index + 1 or not var_list[index]:
        return def_value
    return var_list[index]


def store_vars(*args):
    store(args, TempFile2)


def is_hidden(windowid):
    return "_NET_WM_STATE_HIDDEN" in win_prop(windowid, "_NET_WM_STATE")


def get_simple_tile(wincount):
    rows = wincount - 1
    layout = []
    if rows == 0:
        layout.append(
            (
                OrigX + WinBorder,
                OrigY + WinBorder,
                int(MaxWidth - 2 * WinBorder),
                int(MaxHeight - WinTitle - 2 * WinBorder),
            )
        )
        return layout
    else:
        layout.append(
            (
                OrigX + WinBorder,
                OrigY + WinBorder,
                int(MaxWidth * MwFactor - 2 * WinBorder),
                int(MaxHeight - WinTitle - 2 * WinBorder),
            )
        )
    x = OrigX + int((MaxWidth * MwFactor) + WinBorder)
    width = int((MaxWidth * (1 - MwFactor)) - 2 * WinBorder)
    height = int(MaxHeight / rows - WinTitle - 2 * WinBorder)
    for n in range(0, rows):
        y = OrigY + int((MaxHeight / rows) * (n) + WinBorder)
        layout.append((x, y, width, height))
    return layout


def get_vert_tile(wincount):
    layout = []
    y = OrigY + WinBorder
    width = int(MaxWidth / wincount - 2 * WinBorder)
    height = int(MaxHeight - WinTitle - 2 * WinBorder)
    for n in range(0, wincount):
        x = int(OrigX + n * (MaxWidth / wincount) + WinBorder)
        layout.append((x, y, width, height))
    return layout


def get_horiz_tile(wincount):
    layout = []
    x = OrigX + WinBorder
    height = int(MaxHeight / wincount - WinTitle - 2 * WinBorder)
    width = int(MaxWidth - 2 * WinBorder)
    for n in range(0, wincount):
        y = OrigY + int((MaxHeight / wincount) * (n) + WinBorder)
        layout.append((x, y, width, height))
    return layout


def get_center_tile(wincount):
    layout = []
    width = int(MaxWidth * CFactor)
    height = int(MaxHeight * CFactor - WinTitle)
    x = int(OrigX + MaxWidth / 2 - width / 2)
    y = int(OrigY + MaxHeight / 2 - height / 2 - WinTitle)
    for n in range(0, wincount):
        layout.append((x, y, width, height))
    return layout


def get_left_tile(wincount):
    layout = []
    width = int(MaxWidth * MwFactor)
    height = MaxHeight - WinTitle - WinBorder
    x = OrigX
    y = OrigY
    layout.append((x, y, width, height))
    width = int(MaxWidth * (1 - MwFactor)) - 2 * WinBorder
    x = int(MaxWidth * MwFactor) + OrigX + 2 * WinBorder
    for n in range(0, wincount - 1):
        layout.append((x, y, width, height))
    return layout


def get_right_tile(wincount):
    layout = []
    width = int(MaxWidth * (1 - MwFactor)) - 2 * WinBorder
    height = MaxHeight - WinTitle - WinBorder
    x = int(MaxWidth * MwFactor) + OrigX + 2 * WinBorder
    y = OrigY
    layout.append((x, y, width, height))
    width = int(MaxWidth * MwFactor)
    x = OrigX
    for n in range(0, wincount - 1):
        layout.append((x, y, width, height))
    return layout


def get_max_all(wincount):
    layout = []
    x = OrigX
    y = OrigY
    height = MaxHeight - WinTitle - WinBorder
    width = MaxWidth
    for n in range(0, wincount):
        layout.append((x, y, width, height))
    return layout


def move_active(PosX, PosY, Width, Height):
    os.system(
        " wmctrl -r :ACTIVE: -e 0,"
        + str(PosX)
        + ","
        + str(PosY)
        + ","
        + str(Width)
        + ","
        + str(Height)
    )


def move_win(windowid, PosX, PosY, Width, Height):
    os.system(
        "wmctrl -r "
        + windowid
        + " -e 0,"
        + str(PosX)
        + ","
        + str(PosY)
        + ","
        + str(Width)
        + ","
        + str(Height)
        + " -i"
    )
    os.system("wmctrl -r " + windowid + " -b remove,hidden,shaded -i")


def focus_win(windowid):
    os.system("xdotool windowfocus " + windowid)


def unmaximize_win(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz"
    else:
        command = (
            "wmctrl -r "
            + windowid
            + " -b remove,maximized_vert,maximized_horz -i"
        )
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
        command = (
            "wmctrl -r "
            + windowid
            + " -b add,maximized_vert,maximized_horz -i"
        )
    os.system(command)


def toggle_maximize_win(windowid):
    if windowid == ":ACTIVE:":
        command = "wmctrl -r :ACTIVE: -b toggle,maximized_vert,maximized_horz"
    else:
        command = (
            "wmctrl -r "
            + windowid
            + " -b toggle,maximized_vert,maximized_horz -i"
        )
    os.system(command)


def raise_win(windowid, hidden=False):
    if windowid == ":ACTIVE:":
        os.system("wmctrl -a :ACTIVE: ")
    elif hidden or not is_hidden(windowid):
        os.system("wmctrl -a " + windowid + " -i")


def exclude_win(windowid):
    global IdIncludeSet, IdExcludeSet
    winlist = create_win_list()
    IdExcludeSet.add(windowid)
    if windowid in IdIncludeSet:
        IdIncludeSet.remove(windowid)
    if winlist and windowid in winlist:
        winlist.remove(windowid)
    store_vars(
        Mode,
        MwFactor,
        CFactor,
        IdExcludeSet,
        IdIncludeSet,
        Desktop,
        MaxWinDict,
    )
    arrange_mode(winlist, Mode[Desktop])


def include_win(windowid):
    global IdIncludeSet, IdExcludeSet
    (win_class, win_type, win_state, win_actions) = get_win_props(windowid)
    if not is_includible(
        int(windowid, 16), IdIncludeSet, win_type, win_state, win_actions
    ):
        return
    winlist = create_win_list()
    if windowid in IdExcludeSet:
        IdExcludeSet.remove(windowid)
    IdIncludeSet.add(windowid)
    if windowid not in winlist:
        winlist.append(windowid)
    store_vars(
        Mode,
        MwFactor,
        CFactor,
        IdExcludeSet,
        IdIncludeSet,
        Desktop,
        MaxWinDict,
    )
    arrange_mode(winlist, Mode[Desktop])


def toggle_exclude_win(windowid):
    global IdIncludeSet, IdExcludeSet
    (win_class, win_type, win_state, win_actions) = get_win_props(windowid)
    winlist = create_win_list()
    if windowid in winlist:
        if windowid in IdIncludeSet:
            IdIncludeSet.remove(windowid)
        IdExcludeSet.add(windowid)
        winlist.remove(windowid)
    elif is_includible(
        int(windowid, 16), IdIncludeSet, win_type, win_state, win_actions
    ):
        IdIncludeSet.add(windowid)
        if windowid in IdExcludeSet:
            IdExcludeSet.remove(windowid)
        if windowid not in winlist:
            winlist.append(windowid)
    store_vars(
        Mode,
        MwFactor,
        CFactor,
        IdExcludeSet,
        IdIncludeSet,
        Desktop,
        MaxWinDict,
    )
    arrange_mode(winlist, Mode[Desktop])


def left():
    winlist = create_win_list()
    arrange_mode(winlist, "left")


def right():
    winlist = create_win_list()
    arrange_mode(winlist, "right")


def center():
    winlist = create_win_list()
    active = get_active_window()
    if active in winlist:
        winlist.remove(active)
        winlist.insert(0, active)
    arrange_mode(winlist, "center")


def set_max_win():
    global MaxWinDict
    if MaxWinDict[Desktop] and MaxWinDict[Desktop] == get_active_window():
        maximize_alt()
    else:
        MaxWinDict[Desktop] = 0


def create_win_list(actual=False, notaskbar=True):
    if actual:
        Windows = ActualWinList[Desktop]
    else:
        Windows = WinList[Desktop]
    if not notaskbar:
        return [
            wid
            for wid in Windows
            if not {
                "_NET_WM_STATE_SKIP_TASKBAR",
                "_NET_WM_STATE_HIDDEN",
            }.issubset(win_prop(wid, "_NET_WM_STATE").split(", "))
        ]
    return Windows


def is_changed():
    if Desktop != OldDesktop:
        return True
    if OldWinList == {}:
        return True
    OldWindows = OldWinList[Desktop]
    Windows = WinList[Desktop]
    if Windows != OldWindows:
        return True
    if OldIdExcludeSet != IdExcludeSet:
        return True
    return False


def arrange(layout, windows):
    for win, lay in zip(windows, layout):
        move_win(win, lay[0], lay[1], lay[2], lay[3])
    WinList[Desktop] = windows
    store(WinList, TempFile)


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
        raise_win(win)


def arrange_mode(wins, mode):
    global WinList
    if len(wins):
        WinList[Desktop] = wins
        if Reset or Alt_Reset:
            unmaximize_wins(wins)
            normalize_wins(wins)
            raise_wins(wins)
            raise_win(wins[0])
        if mode == "simple":
            arrange(get_simple_tile(len(wins)), wins)
        elif mode == "horiz":
            arrange(get_horiz_tile(len(wins)), wins)
        elif mode == "vert":
            arrange(get_vert_tile(len(wins)), wins)
        elif mode == "max_all":
            arrange(get_max_all(len(wins)), wins)
        elif mode == "center":
            arrange(get_center_tile(len(wins)), wins)
        elif mode == "left":
            arrange(get_left_tile(len(wins)), wins)
        elif mode == "right":
            arrange(get_right_tile(len(wins)), wins)
        else:
            arrange(get_simple_tile(len(wins)), wins)
    else:
        WinList[Desktop] = []
        store(WinList, TempFile)
    if Reset:
        raise_wins(ExcludedWinList[Desktop])


def simple():
    Windows = create_win_list()
    arrange_mode(Windows, "simple")


def _swap():
    winlist = create_win_list()
    if not winlist:
        return
    active = get_active_window()
    winlist.remove(active)
    winlist.insert(0, active)
    arrange_mode(winlist, Mode[Desktop])


def vert():
    winlist = create_win_list()
    arrange_mode(winlist, "vert")


def horiz():
    winlist = create_win_list()
    arrange_mode(winlist, "horiz")


def _cycle(n):
    winlist = create_win_list()
    if not winlist:
        return
    n = n % len(winlist)
    winlist = winlist[-n:] + winlist[:-n]
    arrange_mode(winlist, Mode[Desktop])
    raise_win(winlist[0])


def cycle_focus(n):
    winlist = create_win_list(actual=True, notaskbar=False)
    if not winlist:
        return
    n = n % len(winlist)
    active = get_active_window()
    if active and active in winlist:
        index = winlist.index(active)
        if index + n < len(winlist):
            index += n
        else:
            index = 0
    else:
        index = 0
    raise_win(winlist[index], hidden=True)
    focus_win(winlist[index])


def maximize():
    maximize_win(":ACTIVE:")
    raise_win(":ACTIVE:")


def maximize_alt():
    global MaxWinDict
    active = get_active_window()
    (win_class, win_type, win_state, win_actions) = get_win_props(active)
    if not active in WinList[Desktop]:
        if {
            "_NET_WM_STATE_MAXIMIZED_HORZ",
            "_NET_WM_STATE_MAXIMIZED_VERT",
        }.isdisjoint(win_state.split(", ")):
            print("maximize")
            maximize()
        else:
            unmaximize()
        return
    if not is_includible(
        int(active, 16), IdIncludeSet, win_type, win_state, win_actions
    ):
        return
    X = OrigX
    Y = OrigY
    Height = MaxHeight - WinTitle - WinBorder
    Width = MaxWidth
    move_win(active, X, Y, Width, Height)
    raise_win(active)
    MaxWinDict[Desktop] = active
    store_vars(
        Mode,
        MwFactor,
        CFactor,
        IdExcludeSet,
        IdIncludeSet,
        Desktop,
        MaxWinDict,
    )


def toggle_maximize():
    toggle_maximize_win(":ACTIVE:")
    raise_win(":ACTIVE:")


def normalize():
    normalize_win(":ACTIVE:")
    raise_win(":ACTIVE:")


def max_all():
    winlist = create_win_list()
    active = get_active_window()
    if active in winlist:
        winlist.remove(active)
        winlist.insert(0, active)
    arrange_mode(winlist, "max_all")


def set_mwfactor(mf):
    mf = getvalue(mf, MinMwFactor, MaxMwFactor)
    store_vars(
        Mode, mf, CFactor, IdExcludeSet, IdIncludeSet, Desktop, MaxWinDict
    )
    return mf


def set_cfactor(cf):
    cf = getvalue(cf, MinCFactor, MaxCFactor)
    store_vars(
        Mode, MwFactor, cf, IdExcludeSet, IdIncludeSet, Desktop, MaxWinDict
    )
    return cf


def _reset():
    _set_mode(Mode[Desktop])


def daemon():
    if is_changed():
        if OldIdExcludeSet != IdExcludeSet:
            for id_index in PropExcludedList:
                exclude = hex(int(id_index[0], 16))
                if exclude in IdExcludeSet and exclude not in OldIdExcludeSet:
                    set_win_props(id_index[0], PropExcludeList[id_index[1]][2])
        _set_mode(Mode[Desktop])


def unmaximize():
    unmaximize_win(":ACTIVE:")
    raise_win(":ACTIVE:")


def _set_mode(mode):
    global Mode
    if mode == "simple":
        simple()
    elif mode == "horiz":
        horiz()
    elif mode == "vert":
        vert()
    elif mode == "max_all":
        max_all()
    elif mode == "center":
        center()
    elif mode == "left":
        left()
    elif mode == "right":
        right()
    else:
        mode = OrigMode[Desktop]
        globals()[mode]()
    set_max_win()
    Mode[Desktop] = mode
    store_vars(
        Mode,
        MwFactor,
        CFactor,
        IdExcludeSet,
        IdIncludeSet,
        Desktop,
        MaxWinDict,
    )


def reset():
    global Reset, MaxWinDict
    Reset = True
    MaxWinDict[Desktop] = 0
    _reset()


def alt_reset():
    global Alt_Reset, MaxWinDict
    Alt_Reset = True
    MaxWinDict[Desktop] = 0
    _reset()


def set_mode(mode):
    global Reset, Mode
    Reset = True
    Mode[Desktop] = mode
    _set_mode(Mode[Desktop])


def swap():
    global Alt_Reset
    Alt_Reset = True
    _swap()


def cycle(n):
    global Alt_Reset
    Alt_Reset = True
    _cycle(n)


def exclude_active():
    active = get_active_window()
    if active:
        exclude_win(active)


def toggle_exclude_active():
    active = get_active_window()
    if active:
        toggle_exclude_win(active)


def include_active():
    active = get_active_window()
    if active:
        include_win(active)


def inc_mwfactor():
    global Alt_Reset, MwFactor, MaxWinDict
    Alt_Reset = True
    MaxWinDict[Desktop] = 0
    MwFactor = set_mwfactor(MwFactor + 0.05)
    if Mode[Desktop] in ("simple", "left", "right"):
        _set_mode(Mode[Desktop])
    else:
        _set_mode("simple")


def dec_mwfactor():
    global Alt_Reset, MwFactor, MaxWinDict
    Alt_Reset = True
    MaxWinDict[Desktop] = 0
    MwFactor = set_mwfactor(MwFactor - 0.05)
    if Mode[Desktop] in ("simple", "left", "right"):
        _set_mode(Mode[Desktop])
    else:
        _set_mode("simple")


def reset_mwfactor():
    global Alt_Reset, MwFactor, MaxWinDict
    Alt_Reset = True
    MaxWinDict[Desktop] = 0
    MwFactor = set_mwfactor(OrigMwFactor)
    if Mode[Desktop] in ("simple", "left", "right"):
        _set_mode(Mode[Desktop])
    else:
        _set_mode("simple")


def dec_cfactor():
    global Alt_Reset, CFactor, MaxWinDict
    Alt_Reset = True
    MaxWinDict[Desktop] = 0
    CFactor = set_cfactor(CFactor - 0.05)
    _set_mode("center")


def inc_cfactor():
    global Alt_Reset, CFactor, MaxWinDict
    Alt_Reset = True
    MaxWinDict[Desktop] = 0
    CFactor = set_cfactor(CFactor + 0.05)
    _set_mode("center")


def reset_cfactor():
    global Alt_Reset, CFactor, MaxWinDict
    Alt_Reset = True
    MaxWinDict[Desktop] = 0
    CFactor = set_cfactor(OrigCFactor)
    _set_mode("center")


def show_usage():
    print(
        """\
    Usage: styler.py [OPTION]
    Options:
             maximize,unmaximize,normalize,toggle_maximize,maximize_alt
             simple,horiz,vert,max_all,center,left,right,
             inc_mwfactor,dec_mwfactor,reset_mwfactor,
             inc_cfactor,dec_cfactor,reset_cfactor,
             exclude,include,toggle_exclude,
             cycle_focus,rcycle_focus,
             swap,cycle,rcycle,
             reset,alt_reset,
             daemon\
             """
    )


def is_main():
    return __name__ == "__main__"


def check_cmd(cmd):
    try:
        if not cmd:
            return
        if cmd[0] == "reset":
            reset()
        elif cmd[0] == "alt_reset":
            alt_reset()
        elif cmd[0] in Modes:
            set_mode(cmd[0])
        elif cmd[0] == "swap":
            swap()
        elif cmd[0] == "cycle":
            cycle(1)
        elif cmd[0] == "rcycle":
            cycle(-1)
        elif cmd[0] == "cycle_focus":
            cycle_focus(1)
        elif cmd[0] == "rcycle_focus":
            cycle_focus(-1)
        elif cmd[0] == "maximize":
            maximize()
        elif cmd[0] == "toggle_maximize":
            toggle_maximize()
        elif cmd[0] == "unmaximize":
            unmaximize()
        elif cmd[0] == "maximize_alt":
            maximize_alt()
        elif cmd[0] == "normalize":
            normalize()
        elif cmd[0] == "exclude":
            exclude_active()
        elif cmd[0] == "include":
            include_active()
        elif cmd[0] == "toggle_exclude":
            toggle_exclude_active()
        elif cmd[0] == "inc_mwfactor":
            inc_mwfactor()
        elif cmd[0] == "dec_mwfactor":
            dec_mwfactor()
        elif cmd[0] == "reset_mwfactor":
            reset_mwfactor()
        elif cmd[0] == "dec_cfactor":
            dec_cfactor()
        elif cmd[0] == "inc_cfactor":
            inc_cfactor()
        elif cmd[0] == "reset_cfactor":
            reset_cfactor()
        else:
            return False
        return True
    except BaseException:
        print(e)
        return False


def check_args(args):
    if len(args) < 2 or args[1] in ("", "-h", "help", "--help"):
        show_usage()
        return
    elif args[1] == "daemon":
        daemon()
    elif not check_cmd(args[1:]):
        print("Invalid Argument '{}'".format(" ".join(args[1:])))
        sys.exit(1)


OldWinList = retrieve(TempFile)
OldVarList = retrieve(TempFile2)
Mode = get_temp_var(OldVarList, 0, OrigMode)
Modes = ("simple", "horiz", "vert", "max_all", "center", "left", "right")
MwFactor = getvalue(
    get_temp_var(OldVarList, 1, OrigMwFactor), MinMwFactor, MaxMwFactor
)
CFactor = getvalue(
    get_temp_var(OldVarList, 2, OrigCFactor), MinCFactor, MaxCFactor
)
OldIdExcludeSet = get_temp_var(OldVarList, 3, set())
OldIdIncludeSet = get_temp_var(OldVarList, 4, set())
OldDesktop = get_temp_var(OldVarList, 5, set())
MaxWinDict = get_temp_var(OldVarList, 6, dict())
(
    Desktop,
    OrigXstr,
    OrigYstr,
    MaxWidthStr,
    MaxHeightStr,
    ActualWinList,
    WinList,
    ExcludedWinList,
    IdExcludeSet,
    IdIncludeSet,
    PropExcludedList,
) = initialize(OldIdExcludeSet, OldIdIncludeSet)
WinList = compare_win_dict(WinList, OldWinList)
MaxWidth = int(MaxWidthStr) - LeftPadding - RightPadding
MaxHeight = int(MaxHeightStr) - TopPadding - BottomPadding
OrigX = int(OrigXstr) + LeftPadding
OrigY = int(OrigYstr) + TopPadding
Reset = False
Alt_Reset = False
if is_main():
    check_args(sys.argv)
