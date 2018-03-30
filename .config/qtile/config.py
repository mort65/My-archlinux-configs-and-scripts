# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, Match, Rule
#from libqtile.config import ScratchPad, DropDown
from libqtile.command import lazy,Client
from libqtile import layout, bar, widget, hook
import os
import subprocess

mod = "mod4"
term = "/usr/bin/urxvt"
home = os.path.expanduser('~')
client=Client()

wm_groups = {
    "luakit" : "2", "Firefox" : "2","Opera" : "2","Google-chrome" : "2",
    "Chromium" : "2","Vivaldi-stable" : "2","Midori" : "2", "Dillo" : "2",
    "Netsurf-gtk3" : "2","QupZilla" : "2", "Uget-gtk" : "2","Tor Browser" : "2",
    "Waterfox" : "2", "UXTerm" : "3","URxvt" : "3","Terminator" : "3",
    "Urxvt-tabbed" : "3","Urxvt" : "3","Termite" : "3", "mlterm" : "3",
    "XTerm" : "3", "Pcmanfm" : "4","Thunar" : "4","dolphin" : "4", "Caja" : "4",
    "Catfish" : "4", "Zathura" : "5", "libreoffice-writer" : "5","libreoffice" : "5",
    "Leafpad" : "5","kate" : "5","Pluma" : "5","Mousepad" : "5",
    "kwrite" : "5", "Geany" : "5","Gedit" : "5","Code" : "5",
    "Atom" : "5", "Gimp" : "6","Gthumb" : "6", "org.kde.gwenview" : "6",
    "Ristretto" : "6","lximage-qt" : "6", "Eom" : "6", "Gpicview" : "6", 
    "vlc" : "7","xv/mplayer" : "7", "Clementine" : "7", "MPlayer" : "7",
    "smplayer" : "7","mpv" : "7", "Gnome-mpv" : "7","Rhythmbox" : "7",
    "Pragha" : "7",  "Steam" : "8","Wine" : "8","Zenity" : "8",
    "PlayOnLinux" : "8", "VirtualBox" : "9", "okular" : "9", "calibre" : "9", 
    "octopi" : "9", "Pamac-updater" : "9", "Pamac-manager" : "9", "Lxtask" : "9", 
    "Dukto" : "9","QuiteRss" : "9", "Filezilla" : "9",
}
wm_roles = {
    "browser" : "2"
}

group_labels = [
    "🏠", "🌎", "",
    "📁", "📓", "",
    "", "🎮", "🌸",
    "🌑", 
]
    
group_names = [ 
    "1", "2", "3",
    "4", "5", "6",
    "7", "8", "9",
    "0",
]
    
group_exclusives = [
    False,False,False,
    False,False,False,
    False,False,False,
    False,
]
group_persists = [
    True, True, True,
    True, True, True,
    True, True, True,
    True,
]
group_inits = [
    True, True, True,
    True, True, True,
    True, True, True,
    True,
]
    
group_layouts = [
    "tile", "max", "monadwide",
    "zoomy", "stack", "zoomy",
    "max", "max", "columns", 
    "bsp",
]

group_matches = [
    None,
    [ Match(wm_class=[
    "luakit","Firefox","Opera","Google-chrome",
    "Chromium","Vivaldi-stable","Midori",
    "Dillo","Netsurf-gtk3","QupZilla",
    "Uget-gtk","Tor Browser","Waterfox",
    ],role=["browser"]),],

    [ Match(wm_class=[
    "UXTerm","URxvt","Terminator",
    "Urxvt-tabbed","Urxvt","Termite",
    "mlterm", "XTerm",
    ]),],

    [ Match(wm_class=[
    "Pcmanfm","Thunar","dolphin",
    "Caja","Catfish",
    ]),],

    [ Match(wm_class=[
    "Zathura","libreoffice-writer","libreoffice",
    "Leafpad","kate","Pluma","Mousepad","kwrite",
    "Geany","Gedit","Code","Atom",
    ],),],

    [ Match(wm_class=[
    "Gimp","Gthumb","org.kde.gwenview",
    "Ristretto","lximage-qt","Eom",
    "Gpicview",
    ]),],

    [ Match(wm_class=[
    "vlc","xv/mplayer","Clementine",
    "MPlayer","smplayer","mpv",
    "Gnome-mpv","Rhythmbox","Pragha",
    ]),],
    
    [ Match(wm_class=[
    "Steam","Wine","Zenity",
    "PlayOnLinux",
    ]),],

    [ Match(wm_class=[
    "VirtualBox","okular","calibre",
    "octopi","Pamac-updater",
    "Pamac-manager","Lxtask",
    "Dukto","QuiteRss",
    "Filezilla",
    ]),],
    None,
]

def window_to_prev_group():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            i = qtile.groups.index(qtile.currentGroup)
            if i > 0:
                qtile.currentWindow.togroup(qtile.groups[i - 1].name)
            else:
                qtile.currentWindow.togroup(qtile.groups[len(qtile.groups) - 1].name)
    return __inner

def window_to_next_group():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            i = qtile.groups.index(qtile.currentGroup)
            if i < len(qtile.groups) - 1:
                qtile.currentWindow.togroup(qtile.groups[i + 1].name)
            else:
                qtile.currentWindow.togroup(qtile.groups[0].name)
    return __inner

def window_to_prev_screen():
    @lazy.function
    def _inner(qtile):
        if qtile.currentScreen is not None:
            if qtile.currentWindow is not None:
                i = qtile.screens.index(qtile.currentScreen)
                if i > 0:
                    qtile.currentWindow.togroup(qtile.screens[i - 1].group.name)
                else:
                    qtile.currentWindow.togroup(qtile.screens[len(qtile.screens) - 1].group.name)
    return __inner

def window_to_next_screen():
    @lazy.function
    def _inner(qtile):
        if qtile.currentScreen is not None:
            if qtile.currentWindow is not None:
                i = qtile.screens.index(qtile.currentScreen)
                if i < len(qtile.screens) - 1:
                    qtile.currentWindow.togroup(qtile.screens[i + 1].group.name)
            else:
                qtile.currentWindow.togroup(qtile.screens[0].group.name)
    return __inner
    

def get_group_key():
    return client.group.info()['name']

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "h", lazy.layout.left()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),

    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),

    # Switch window focus to other pane(s) of stack
    Key(["mod1"], "Tab", lazy.layout.next()),
    Key(["mod1"], "space", lazy.layout.previous()),
    
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),
   
    Key([mod, "shift"], "Left", window_to_prev_group()),
    Key([mod, "shift"], "Right", window_to_next_group()),
   
    Key([mod], "Left", lazy.screen.prev_group()),
    Key([mod], "Right", lazy.screen.next_group()),
    
    Key([mod, "control"], "l", 
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key([mod, "control"], "h", 
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),

    Key([mod, "control"], "k", 
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    
    Key([mod, "control"], "j", 
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    
    Key([mod], "m", 
        lazy.layout.maximize(),
    ),
    
    Key([mod], "n", 
        lazy.layout.normalize(),
    ),
    
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),

    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    
    # Swap panes of split stack
    Key([mod, "shift"], "space", 
        lazy.layout.rotate()
    ),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(term)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "space", lazy.prev_layout()),
    Key([mod, "shift"], "x", lazy.window.kill()),

    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "Pause", lazy.shutdown()),
    Key([mod, "shift"], "Scroll_Lock", lazy.spawn("/usr/bin/slock")),
    Key([mod, "shift", "control"], "Print", lazy.spawn("/usr/bin/systemctl -i suspend")),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "g", lazy.switchgroup()),
    
    # Applications
    Key([mod], "d", lazy.spawn("/usr/bin/rofi -modi run,drun -show drun run")),
    Key([mod], "e", lazy.spawn("/usr/bin/leafpad")),
    Key([mod, "shift"], "e", lazy.spawn("/usr/bin/geany")),
    Key([mod], "Home", lazy.spawn("/usr/bin/pcmanfm")),
    Key([mod, "shift"], "Home", lazy.spawn(term + " -e '/usr/bin/ranger'")),
    Key([mod], "p", lazy.spawn("/usr/bin/pragha")),
    Key([mod], "c", lazy.spawn(term + " -e '/usr/bin/cmus'")),
    Key([mod], "w", lazy.spawn("/usr/bin/firefox")),
    Key([mod], "i", lazy.spawn("/usr/bin/pamac-manager")),

    #Media player controls
    Key([], "XF86AudioPlay", lazy.spawn("/usr/bin/playerctl play")),
    Key([], "XF86AudioPause", lazy.spawn("/usr/bin/playerctl pause")),
    Key([], "XF86AudioNext", lazy.spawn("/usr/bin/playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("/usr/bin/playerctl previous")),
    
    # Screenshot
    Key([], "Print", lazy.spawn("/usr/bin/scrot " + home + "/Pictures/Screenshots/screenshot_%Y_%m_%d_%H_%M_%S.png")),
    
    
    # Pulse Audio controls
    Key([], "XF86AudioMute", lazy.spawn("/usr/bin/pactl set-sink-mute alsa_output.pci-0000_00_1b.0.analog-stereo toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("/usr/bin/pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("/usr/bin/pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo +5%"))
]

layout_style = {
    'font' : 'ubuntu',
    'margin' : 2,
    'border_width' : 1,
    'border_normal' : '000000',
    'border_focus' : '0000FF',
    
}

layouts = [
    layout.Tile(**layout_style),
    layout.Columns(num_columns=2,autosplit=True,**layout_style),
    layout.Stack(num_stacks=1,**layout_style),
    layout.MonadTall(**layout_style),
    layout.MonadWide(**layout_style),
    layout.Bsp(**layout_style),
   #layout.Matrix(**layout_style),
    layout.Zoomy(**layout_style),
    layout.Max(**layout_style),
    #layout.Floating(**layout_style),
]

groups = []


for i in range(len(group_names)):
    groups.append(
    Group(
    name = group_names[i],
    matches = group_matches[i],
    exclusive = group_exclusives[i],
    layout = group_layouts[i].lower(),
    persist = group_persists[i],
    init = group_inits[i],
    label = group_labels[i],
    ))

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])
    
#groups.append(   
#    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
#        DropDown("term", "urxvt", opacity=0.9),

        # define another terminal exclusively for qshell at different position
#        DropDown("qshell", "urxvt -hold -e qshell",
#                 x=0.05, y=0.4, width=0.9, height=0.6, opacity=0.9,
#                 on_focus_lost_hide=True) ]), 
#)

#keys.extend ([
#    # Scratchpad
#    # toggle visibiliy of above defined DropDown named "term"
#    Key([], 'F11', lazy.group['scratchpad'].dropdown_toggle('term')),
#    Key([], 'F12', lazy.group['scratchpad'].dropdown_toggle('qshell')),

#])



widget_defaults = dict(
    font='ubuntu',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def get_jdate():
    return '📅 ' + subprocess.check_output(['/usr/bin/jdate', '+%h %D']).decode('utf-8').strip()

def get_time():
    return ' ⏰ ' + subprocess.check_output(['/usr/bin/jdate', '+%I:%M %p']).decode('utf-8').strip()

def get_jdatetime():
    return (get_jdate() + get_time())

def get_updates():
    return subprocess.check_output([home + '/.script/qtile-totalupdatesavail']).decode('utf-8').strip()

def get_keyboardlayout():
    return '⌨ ' + subprocess.check_output([home + '/.script/qtile-keyboardlayout']).decode('utf-8').strip()

def get_freemem():
    return '🎫 ' + subprocess.check_output([home + '/bin/totalfreemem','-g','2']).decode('utf-8').strip()

def get_freeswap():
    return '🔃 ' + subprocess.check_output([home + '/bin/totalfreeswap','-g','2']).decode('utf-8').strip()

def get_ctemp():
    return '🅒 ' + subprocess.check_output([home + '/bin/ctemp','--max']).decode('utf-8').strip()
def get_gtemp():
    return '🅖 ' + subprocess.check_output([home + '/bin/gtemp']).decode('utf-8').strip()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.8),
                widget.GenPollText(func=get_group_key, update_interval=0.5, foreground='DFE8EB',padding=1,fontsize=12),
                widget.GroupBox(active='EFF8FB',inactive='8F888B',
                                this_current_screen_border='00BCD4',
                                this_screen_border='00BCD4',
                                highlight_method='line',
                                highlight_color=['20262A','060A0F']
                               ),
                widget.Prompt(fontsize=13,cursor_color='FFFFFF',foreground='FAF0A8',background='271B1B'),
                widget.WindowName(foreground='89BAAC'),
                widget.Net(interface='enp3s0',foreground='FFAAFF'),
                widget.GenPollText(func=get_ctemp, update_interval=5, foreground='88D2FF'),
                widget.GenPollText(func=get_gtemp, update_interval=5, foreground='88D2FF'),
                widget.GenPollText(func=get_freemem, update_interval=5, foreground='00FFBB'),
                widget.GenPollText(func=get_freeswap, update_interval=5, foreground='00FFBB'),
                widget.GenPollText(func=get_updates, update_interval=5, foreground='FFFF7F'),
                widget.GenPollText(func=get_keyboardlayout, update_interval=1, foreground='FFAA7F'),
                widget.GenPollText(func=get_jdatetime, update_interval=1, foreground='B1D0FF'),
                widget.Systray(),
                widget.Spacer(length=3)
            ],
            22,
            background=['20262A','060A0F'],
            opacity=0.90,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wmclass': 'Dukto'},  # Dukto
    {'wmclass': 'Guake'},  # Guake
    {'wmclass': 'Tilda'},  # Tilda
    {'wmclass': 'yakuake'},  #yakuake
    
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.client_managed
def goto_group(window):
    if (window.window.get_wm_class()[1] in wm_groups.keys()
    or window.window.get_wm_window_role() in wm_roles.keys()):
        window.group.cmd_toscreen()


@hook.subscribe.client_new
def set_floating(window):
    floating_types = ["notification", "toolbar", "splash", "dialog"]
    floating_roles = ["EventDialog", "Msgcompose", "Preferences"]
    floating_names = ["Terminator Preferences", "Search Dialog",
                      "Module", "Goto", "IDLE Preferences", "Sozi",
                      "Create new database",
                     ]
    if (window.window.get_wm_type() in floating_types
        or window.window.get_wm_window_role() in floating_roles
        or window.window.get_name() in floating_names
        or window.window.get_wm_transient_for()):
        window.floating = True

@hook.subscribe.client_new
def libreoffice_dialogues(window):
    if((window.window.get_wm_class() == ('VCLSalFrame', 'libreoffice-calc')) or
    (window.window.get_wm_class() == ('VCLSalFrame', 'LibreOffice 3.4'))):
        window.floating = True

# Qtile startup commands, not repeated at qtile restart
@hook.subscribe.startup_once
def autostart():
    from datetime import datetime
    try:
        subprocess.call([home + '/.config/qtile/autostart.sh'])
    except:
        with open('log file', 'w') as f:
            f.write(
                datetime.now().strftime('%Y-%m-%dT%H:%M') +
                'There was an error\n')
