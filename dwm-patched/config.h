/* See LICENSE file for copyright and license details. */
#include <X11/XF86keysym.h>

/*Macros->*/
/*Tag bit-mask macros*/
#define TAG(N) (1 << (N - 1))
#define TAGS2(A, B) (TAG(A) | TAG(B))
#define TAGS3(A, B, C) (TAG(A) | TAG(B) | TAG(C))

/* Rule macros*/
#define CLASS(C) (C), NULL, NULL
#define INSTANCE(I) NULL, (I), NULL
#define TITLE(T) NULL, NULL, (T)
#define CLASS_W_TITLE(C, T) (C), NULL, (T)
/*->Macros*/

/* appearance */
static const unsigned int borderpx  = 1;        /* border pixel of windows */
static const unsigned int snap      = 32;       /* snap pixel */
static const unsigned int minwsz    = 20;       /* Minimal heigt of a client for smfact */
static const unsigned int gappx     = 3;        /* gap pixel between windows */
static const unsigned int systraypinning = 0;   /* 0: sloppy systray follows selected monitor, >0: pin systray to monitor X */
static const unsigned int systrayspacing = 2;   /* systray spacing */
static const int systraypinningfailfirst = 1;   /* 1: if pinning fails, display systray on the first monitor, False: display systray on the last monitor*/
static const int showsystray        = 1;     /* 0 means no systray */
static const int showbar            = 1;        /* 0 means no bar */
static const int topbar             = 1;        /* 0 means bottom bar */
static const char buttonbar[]       = "𝍤";
static const char *fonts[]          = { "monospace:size=10" };
static const char dmenufont[]       = "monospace:size=10";

static const char col_gray1[]       = "#222222";
static const char col_gray2[]       = "#444444";
static const char col_gray3[]       = "#bfbfbf";
static const char col_gray4[]       = "#999999";
static const char col_white[]       = "#ffffff";
static const char col_red[]         = "#ff0066";
static const char col_pink[]        = "#a53076";
static const char col_blue[]        = "#305fa5";
static const char col_blue2[]       = "#0099ff";
static const char col_green[]       = "#66ff00";
static const char col_yellow[]      = "#ffff00";
static const char col_purple[]      = "#9900ff";
static const char col_purple2[]     = "#47328c";
static const char col_orange[]      = "#ff6600";
static const char *colors[][7]      = {
	/*               fg         bg          border     float      sticky      permanent	mark */
	[SchemeNorm] = { col_gray3, col_gray1,  col_gray2, col_gray2, col_gray2,  col_gray2, col_gray4 },
	[SchemeSel]  = { col_white, col_blue,  col_blue2, col_green,  col_yellow, col_purple, col_orange },
	[SchemeUrg]  = { col_white, col_pink, col_red,   col_red,   col_red,    col_red, col_red },
	[SchemeBtn]  = { col_white, col_purple2, col_red,   col_red,   col_red,    col_red, col_red },
};

/* tagging */
static const char *tags[] = { "1", "2", "3", "4", "5", "6", "7", "8", "9" };


static const Rule rules[] = {
	/* xprop(1):
	 *	WM_CLASS(STRING) = instance, class
	 *	WM_NAME(STRING) = title
	 */
	/*Match condition   Tags   Center   Float   Permanent   Terminal   Swallow   Monitor*/
	{ CLASS("Gimp"),  0,   1,   0,   0 },
        { CLASS("URxvt|Urxvt-tabbed"),  0,   0,   0,   1,   1,   1,   0 },
        { CLASS("UXTerm|XTerm|rxvt|Lxterminal"),  0,   0,   0,   0,   1,   1,   0 },
	{ CLASS("vlc|smplayer|mpv|smplayer"),   TAG(1)|TAG(3)|TAG(4),   0,   0,   0,   0,   0 },
	{ CLASS("Firefox|Chromium|Google-chrome|Vivaldi-stable"),   TAG(2),0,   0,   0,   0 },
        { CLASS("Thunar|Pcmanfm|pcmanfm-qt"),   TAG(3),   0,   0,   0 },
	{ CLASS("Pragha"),  TAG(5) ,  0,    0,   0 },
        { CLASS("Geany|Leafpad"),   TAG(6),   0,   0,   0 },
	{ CLASS("Steam"),  TAG(7),   0,   0,   0 },
        { CLASS("VirtualBox"),   TAG(8),   0,   0,   0 },

        /*Floating windows*/
        { CLASS("St"),  0,   1,   1,   0,   1,   1,   0 },
	{ CLASS("Nitrogen|Dukto|Galculator|lxsu|lxsudo|Gpick"),   0,   0,   1,   0,   0,   0 },
        { TITLE("File Operation Progress"),   0,   0,   1,   0,   0 },
        { TITLE("Module"),   0,   1,   0 },
        { TITLE("Search Dialog"),   0,   0,   1,   0,   0 },
        { TITLE("Goto"),  0,    0,   1,   0,   0 },
        { TITLE("IDLE Preferences"),   0,   0,   1,   0,   0 },
        { TITLE("Preferences"),   0,   0,   1,   0,   0 },
        { TITLE("File Transfer"),   0,   0,   1,   0,   0 },
        { TITLE("branchdialog"),   0,   0,   1,   0,   0 },
        { TITLE("pinentry"),   0,   0,   1,   0,   0,   0 },
        { TITLE("confirm"),   0,   0,   1,   0,   0 },
        { INSTANCE("eog"),   0,   0,   1,    0,   0 },
	{ CLASS_W_TITLE("Firefox","Firefox Preferences"),   TAG(2),   0,   1,   0,   0 },
	{ CLASS_W_TITLE("Firefox","Library"),   TAG(2),  0,   1,   0,   0 },
};

/* layout(s) */
static const float mfact     = 0.50; /* factor of master area size [0.05..0.95] */
static const float smfact     = 0.00; /* factor of tiled clients [0.00..0.95] */
static const int nmaster     = 1;    /* number of clients in master area */
static const int resizehints = 0;    /* 1 means respect size hints in tiled resizals */

/**
 * Layout variable names
 *
 * These enum elements can be re-arranged to change the default layout.
 * Deletions from or additions to this list should be accompanied with changes
 * to the "layouts" variable.
 */
enum {
    tile_layout,
    floating_layout,
    monocle_layout,
    col_layout,
    tcl_layout,
    deck_layout,
    bstack_layout,
    bstackh_layout,
    gaplessg_layout,
    horizg_layout,
    spiral_layout,
    dwindle_layout,
};

#include "fibonacci.c"
#include "gaplessgrid.c"
#include "horizgrid.c"
#include "layouts.c"
#include "tcl.c"
static const Layout layouts[] = {
	/* symbol     arrange function */
	[tile_layout]     = { "[]=",      tile },    /* first entry is default */
	[floating_layout] = { "><>",      NULL },    /* no layout function means floating behavior */
	[monocle_layout]  = { "[M]",      monocle },
	[col_layout]      = { "|||",      col },
	[tcl_layout]      = { "H^H",      tcl },
	[deck_layout]     = { "H[]",      deck },
	[bstack_layout]   = { "TTT",      bstack },
        [bstackh_layout]  = { "===",      bstackhoriz },
	[gaplessg_layout] = { "HHH",      gaplessgrid },
	[horizg_layout]   = { "###",      horizgrid },
 	[spiral_layout]   = { "[@]",      spiral },
 	[dwindle_layout]  = { "[\\]",      dwindle },
	                    { NULL,       NULL },
};

/**
 * Default layouts, nmaster mfact and showbar values for each tag
 *
*/
static const float deflts[][5] = {
	{ tile_layout, floating_layout, nmaster, mfact, showbar },
	{ tcl_layout, floating_layout, nmaster, mfact, showbar },
	{ bstack_layout, floating_layout, nmaster, mfact, showbar },
	{ monocle_layout, floating_layout, nmaster, mfact, showbar },
	{ gaplessg_layout, floating_layout, nmaster, mfact, showbar },
	{ col_layout, floating_layout, 2, mfact, showbar },
	{ monocle_layout, floating_layout, nmaster, mfact, showbar },
	{ deck_layout, floating_layout, nmaster, mfact, showbar },
	{ horizg_layout, floating_layout, nmaster, mfact, showbar },
};



/**
 * Rules hook
 *
 * This function is called once applyrules is done processing a client with the
 * client in question passed as an argument.
 */
void ruleshook(Client *c)
{
    // Certain floating Wine windows always get positioned off-screen. When
    // that happens, this code will center them.
    if (!strcmp(c->class, "Wine") && c->x < 1) {
        c->x = c->mon->mx + (c->mon->mw / 2 - WIDTH(c) / 2);
        c->y = c->mon->my + (c->mon->mh / 2 - HEIGHT(c) / 2);
    }

    // Mark windows that get created offscreen as urgent.
    if (!scanning && !ISVISIBLE(c)) {
        seturgent(c, 1);
    }

}

#include "tagall.c"

/* key definitions */
#define MODKEY Mod4Mask
#define ALTMODKEY Mod1Mask
#define TAGKEYS(KEY,TAG) \
	{ KeyPress,   MODKEY,                          KEY,      view,           {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ControlMask,              KEY,      toggletag,      {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ShiftMask,                KEY,      tag,            {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ALTMODKEY,                KEY,      toggleview,     {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ControlMask|ShiftMask,    KEY,      tagall,         {.ui = 1 << TAG} }, \
	{ KeyPress,   ALTMODKEY|ControlMask|ShiftMask, KEY,      tagallfloating, {.ui = 1 << TAG} },

/* helper for spawning shell commands in the pre dwm-5.0 fashion */
#define SHCMD(cmd) { .v = (const char*[]){ "/bin/sh", "-c", cmd, NULL } }

/* commands */
static char dmenumon[2] = "0"; /* component of dmenucmd, manipulated in spawn() */
static const char *dmenucmd[] = { "dmenu_run", "-m", dmenumon, "-fn", dmenufont, "-nb", col_gray1, "-nf", col_gray3, "-sb", col_blue, "-sf", col_white, NULL };
static const char *roficmd[] = { "rofi", "-modi", "combi#window#run#drun", "-show", "combi", "-combi-modi", "window#run#drun", NULL };
static const char *termcmd[]  = { "mlterm", NULL, NULL, NULL, NULL, "1", NULL };
static const char *termcmd1[]  = { "urxvt", NULL, NULL, NULL, NULL, "1", NULL };
static const char *termcmd2[]  = { "st", NULL, NULL, NULL, NULL, "1", NULL };
static const char scratchpadname[] = "scratchpad";
static const char *scratchpadcmd[] = { "st", "-t", scratchpadname, "-g", "120x34", NULL };
static const char *firefox[] = { "firefox", NULL, NULL, NULL, "Firefox", NULL, NULL};
static const char *filemanager[] = { "pcmanfm", NULL, NULL, NULL, "Pcmanfm", NULL, NULL};
static const char *ranger[] = { "urxvt", "-e", "ranger", NULL, NULL, NULL, NULL };
static const char *nnn[] = { "urxvt", "-e", "nnnstart", NULL, NULL, NULL, NULL };
static const char *cmus[] = { "mlterm", "-e", "cmus", NULL, NULL, "5", NULL};
static const char *musicplayer[] = { "pragha", NULL, NULL, NULL, "Pragha", NULL, NULL};
static const char *texteditor[] = { "geany", NULL, NULL, NULL, "Geany", NULL, NULL };
static const char *volumeup[] = { "amixer", "set", "Master", "5%+", NULL };
static const char *volumedown[] = { "amixer", "set", "Master", "5%-", NULL };
static const char *volumemute[] = { "amixer", "set", "Master", "toggle", NULL };
static const char *audionext[] = { "playerctl", "next", NULL };
static const char *audioprev[] = { "playerctl", "previous", NULL };
static const char *audiostop[] = { "playerctl", "stop", NULL };
static const char *audioplay[] = { "playerctl", "play-pause", NULL };
static const char *lock[] = { "slock", NULL };
static const char *lxtask[] = { "lxtask", NULL, NULL, NULL, "Lxtask", NULL, NULL };
static const char *htop[] = { "mlterm", "-e", "htop", NULL, NULL, NULL, NULL };

#include "selfrestart.c"
#include "moveresize.c"
#include "shiftview.c"
#include "zoomswap.c"
static Key keys[] = {
/*	 type            modifier                         key                function        argument */
 	{KeyPress,	 MODKEY,                          32,              spawn,          {.v = dmenucmd } }, // o
	{ KeyPress,	 MODKEY,                          33,              spawn,          {.v = roficmd } }, // p
	{ KeyPress,	 MODKEY|ControlMask,              36,              runorraise,     {.v = termcmd } }, // Return
	{ KeyPress,	 MODKEY|ControlMask,              28,              spawn,          {.v = termcmd } }, // t
	{ KeyPress,	 MODKEY|ShiftMask,                36,              runorraise,     {.v = termcmd1 } }, // Return
	{ KeyPress,	 MODKEY|ShiftMask,                28,              spawn,          {.v = termcmd1 } }, // t
	{ KeyPress,	 MODKEY|ALTMODKEY,                36,              runorraise,     {.v = termcmd2 } }, // Return
	{ KeyPress,	 MODKEY|ALTMODKEY,                28,              spawn,          {.v = termcmd2 } }, // t
        { KeyPress,	 MODKEY,                          49,              togglescratch,  {.v = scratchpadcmd } }, // grave `
	{ KeyPress,	 MODKEY,                          56,              togglebar,      {0} }, // b
	{ KeyPress,	 MODKEY,                          52,              toggletags,     {0} }, // z
	{ KeyPress,	 MODKEY|ShiftMask,                56,              spawn,          SHCMD("~/.script/dwm-toggle_dzen") }, // b
	{ KeyPress,	 MODKEY|ShiftMask,                44,              rotatestack,    {.i = +1 } }, // j
	{ KeyPress,	 MODKEY|ShiftMask,                45,              rotatestack,    {.i = -1 } }, // k
	{ KeyPress,	 MODKEY,                          44,              focusstack,     {.i = +1 } }, // j
	{ KeyPress,	 MODKEY,                          45,              focusstack,     {.i = -1 } }, // k
	{ KeyPress,	 MODKEY,                          31,              incnmaster,     {.i = +1 } }, // i
	{ KeyPress,	 MODKEY,                          40,              incnmaster,     {.i = -1 } }, // d
        { KeyPress,	 MODKEY,                          47,              shiftview,      {.i = -1 } }, // semicolon ;
        { KeyPress,	 MODKEY,                          48,              shiftview,      {.i = +1 } }, // apostrophe '
        { KeyPress,	 MODKEY,                          43,              setmfact,       {.f = -0.05} }, // h
	{ KeyPress,	 MODKEY,                          46,              setmfact,       {.f = +0.05} }, // l
	{ KeyPress,	 MODKEY|ShiftMask,                43,              setsmfact,      {.f = +0.05} }, // h
	{ KeyPress,	 MODKEY|ShiftMask,                46,              setsmfact,      {.f = -0.05} }, // l
	{ KeyPress,	 MODKEY,                          36,              zoom,           {0} }, // Return
	{ KeyPress,	 MODKEY,                          23,              view,           {0} },// Tab
	{ KeyPress,	 MODKEY|ShiftMask,                54,              killclient,     {0} }, // c
	{ KeyPress,	 MODKEY,                          28,              setlayout,      {.v = &layouts[0]} }, // t
	{ KeyPress,	 MODKEY,                          41,              setlayout,      {.v = &layouts[1]} }, // f
	{ KeyPress,	 MODKEY,                          58,              setlayout,      {.v = &layouts[2]} }, // m
	{ KeyPress,	 MODKEY,                          54,              setlayout,      {.v = &layouts[3]} }, // c
	{ KeyPress,	 MODKEY,                          26,              setlayout,      {.v = &layouts[4]} }, // e
	{ KeyPress,	 MODKEY,                          55,              setlayout,      {.v = &layouts[5]} }, // v
	{ KeyPress,	 MODKEY,                          29,              setlayout,      {.v = &layouts[6]} }, // y
	{ KeyPress,	 MODKEY,                          30,              setlayout,      {.v = &layouts[7]} }, // u
	{ KeyPress,	 MODKEY,                          42,              setlayout,      {.v = &layouts[8]} }, // g
	{ KeyPress,	 MODKEY,                          27,              setlayout,      {.v = &layouts[9]} }, // r
	{ KeyPress,	 MODKEY,                          39,              setlayout,      {.v = &layouts[10]} }, // s
	{ KeyPress,	 MODKEY,                          25,              setlayout,      {.v = &layouts[11]} }, // w
	{ KeyPress,	 MODKEY,		          59,              cyclelayout,    {.i = -1 } }, // comma ,
	{ KeyPress,	 MODKEY,                          60,              cyclelayout,    {.i = +1 } }, // period .
	{ KeyPress,	 MODKEY,                          65,              setlayout,      {0} }, // space
	{ KeyPress,	 MODKEY|ShiftMask,                65,              togglefloating, {0} }, // space
	{ KeyPress,	 MODKEY,                          57,              togglesticky,   {0} }, // n
	{ KeyPress,	 MODKEY|ShiftMask,                57,              togglepermanent,{0} }, // n
	{ KeyPress,	 MODKEY|ShiftMask,                58,              center,         {0} }, // m
	{ KeyPress,	 MODKEY,                          19,              view,           {.ui = ~0 } }, // 0
	{ KeyPress,	 MODKEY|ShiftMask,                19,              tag,            {.ui = ~0 } }, // 0
	{ KeyPress,	 MODKEY|ControlMask|ShiftMask,    19,              tagall,         {.ui = ~0 } }, // 0
	{ KeyPress,	 ALTMODKEY|ControlMask|ShiftMask, 19,              tagallfloating, {.ui = ~0 } }, // 0
	{ KeyPress,	 MODKEY|ALTMODKEY,                59,              focusmon,       {.i = -1 } }, // comma ,
	{ KeyPress,	 MODKEY|ALTMODKEY,                60,              focusmon,       {.i = +1 } }, // period .
	{ KeyPress,	 MODKEY|ShiftMask,                59,              tagmon,         {.i = -1 } }, // comma ,
	{ KeyPress,	 MODKEY|ShiftMask,                60,              tagmon,         {.i = +1 } }, // period .
	{ KeyPress,	 MODKEY,                          34,              togglemark,     {0} }, // bracketleft [
	{ KeyPress,	 MODKEY,                          35,              swapfocus,      {0} }, // bracketright ]
	{ KeyPress,	 MODKEY,                          51,              swapclient,     {0} }, // backslash
	{ KeyPress,	 ALTMODKEY,                       23,              swapfocused,    {0} }, // Tab
	{ KeyPress,	 Mod4Mask,			  111,	           moveresize,     {.v = "0x -25y 0w 0h"} }, // Up
	{ KeyPress,	 MODKEY,			  116,	           moveresize,     {.v = "0x 25y 0w 0h"} }, // Down
	{ KeyPress,	 MODKEY,			  113,	           moveresize,     {.v = "-25x 0y 0w 0h"} }, // Left
	{ KeyPress,	 MODKEY,			  114,	           moveresize,     {.v = "25x 0y 0w 0h"} }, // Right
	{ KeyPress,	 MODKEY|ShiftMask,		  111,	           moveresize,     {.v = "0x 0y 0w -25h"} }, // Up
	{ KeyPress,	 MODKEY|ShiftMask,	          116,             moveresize,     {.v = "0x 0y 0w 25h"} }, // Down
	{ KeyPress,	 MODKEY|ShiftMask,	          113,             moveresize,     {.v = "0x 0y -25w 0h"} }, // Left
	{ KeyPress,	 MODKEY|ShiftMask,		  114,             moveresize,     {.v = "0x 0y 25w 0h"} }, // Right
        { KeyPress,	 MODKEY|ShiftMask,                27,              self_restart,   {0} }, // r
	/*{ KeyPress,	 MODKEY|ShiftMask,                24,              quit,           {0} },*/ // q
	{ KeyPress,	 MODKEY|ControlMask|ShiftMask,    24,              quit,           {1} }, // q
	{ KeyPress,	 MODKEY|ShiftMask,                78,              spawn,          {.v = lock} }, // scroll_lock
	{ KeyPress,	 MODKEY|ShiftMask,                24,              spawn,          SHCMD("~/.script/dwm-logout_menu") }, // q
	{ KeyPress,	 MODKEY|ShiftMask,                127,             spawn,          SHCMD("~/.script/dwm-rofi_runit_exit_menu") }, // Pause
	{ KeyPress,	 MODKEY,                          53,              spawn,          SHCMD("xkill") }, // x
	{ KeyPress,      MODKEY|ControlMask|ShiftMask,    53,              killunsel,      {0} }, // x
	{ KeyPress,	 MODKEY|ControlMask,              27,              spawn,          {.v = ranger} }, // r
	{ KeyPress,	 MODKEY|ControlMask,              57,              spawn,          {.v = nnn} }, // n
	{ KeyPress,	 MODKEY|ControlMask,              58,              runorraise,     {.v = cmus} }, // m
	{ KeyPress,	 MODKEY|ControlMask,              33,              runorraise,     {.v = musicplayer} }, // p
        { KeyPress,	 MODKEY|ControlMask,              110,             runorraise,     {.v = filemanager} }, // Home
        { KeyPress,	 MODKEY|ControlMask,              26,              runorraise,     {.v = texteditor} },
        { KeyPress,	 MODKEY|ControlMask,              119,             runorraise,     {.v = lxtask} }, // Delete
        { KeyPress,	 MODKEY,                          119,             spawn,          {.v = htop} }, // Delete
        { KeyPress,	 MODKEY,	                  67,              spawn,          SHCMD("jgmenu_run") }, // F1
        { KeyPress,	 MODKEY,	                  68,              spawn,          SHCMD("~/.script/dwm-app_menu") }, // F2
	{ KeyPress,	 MODKEY,	                  69,              spawn,          SHCMD("gksudo") }, // F3
        { KeyRelease,	 MODKEY,                          107,             spawn,          SHCMD("~/bin/winshot") }, // Print
        { KeyRelease,	 0,                               107,             spawn,          SHCMD("~/bin/screenshot") }, // Print
	{ KeyPress,	 0,                               123,             spawn,          {.v = volumeup} }, // XF86XK_AudioRaiseVolume
	{ KeyPress,	 0,                               122,             spawn,          {.v = volumedown} }, //XF86XK_AudioLowerVolume
	{ KeyPress,	 0,                               121,             spawn,          {.v = volumemute} }, // XF86XK_AudioMute
	{ KeyPress,	 0,                               171,             spawn,          {.v = audionext} }, // XF86XK_AudioNext
	{ KeyPress,	 0,                               173,             spawn,          {.v = audioprev} }, // XF86XK_AudioPrev
	{ KeyPress,	 0,                               174,             spawn,          {.v = audiostop} }, // XF86XK_AudioStop
	{ KeyPress,	 0,                               172,             spawn,          {.v = audioplay} }, // XF86XK_AudioPlay
	{ KeyPress,	 0,                               180,             runorraise,     {.v = firefox} }, // XF86XK_HomePage
	{ KeyPress,	 0,                               225,             spawn,          SHCMD("xdg-open 'https://www.google.com/'") }, // XF86Search
	{ KeyPress,	 0,                               163,             spawn,          SHCMD("xdg-open 'https://www.google.com/gmail/'") }, // XF86Mail
	{ KeyPress,	 0,                               164,             spawn,          {.v = filemanager} }, // XF86Favorites
        { KeyPress,	 MODKEY|ControlMask,              25,              runorraise,     {.v = firefox} }, // w
	TAGKEYS(                        10,                      0) // 1
	TAGKEYS(                        11,                      1) // 2
	TAGKEYS(                        12,                      2) // 3
	TAGKEYS(                        13,                      3) // 4
	TAGKEYS(                        14,                      4) // 5
	TAGKEYS(                        15,                      5) // 6
	TAGKEYS(                        16,                      6) // 7
	TAGKEYS(                        17,                      7) // 8
	TAGKEYS(                        18,                      8) // 9
};

/* button definitions */
/* click can be ClkTagBar, ClkLtSymbol, ClkStatusText, ClkWinTitle, ClkClientWin, or ClkRootWin */
static Button buttons[] = {
	/* click                event mask      button          function        argument */
	/* { ClkButton,		0,		Button1,	spawn,		SHCMD("~/.script/dwm-app_menu") }, */
	{ ClkButton,		0,		Button1,	spawn,		SHCMD("jgmenu_run") },
	{ ClkButton,		0,		Button2,	spawn,		SHCMD("~/.script/dwm-app_menu") },
	{ ClkButton,		0,		Button3,	toggletags,     {0} },
	{ ClkLtSymbol,          0,              Button1,        cyclelayout,    {.i = +1} },
	{ ClkLtSymbol,          0,              Button2,        setlayout,      {0} },
	{ ClkLtSymbol,          0,              Button3,        cyclelayout,    {.i = -1} },
	{ ClkStatusText,        0,              Button2,        spawn,          {.v = termcmd} },
	{ ClkClientWin,         MODKEY,         Button1,        movemouse,      {0} },
	{ ClkClientWin,         MODKEY,         Button2,        togglefloating, {0} },
	{ ClkClientWin,         MODKEY,         Button3,        resizemouse,    {0} },
	{ ClkTagBar,            0,              Button1,        view,           {0} },
	{ ClkTagBar,            0,              Button3,        toggleview,     {0} },
	{ ClkTagBar,            MODKEY,         Button1,        tag,            {0} },
	{ ClkTagBar,            MODKEY,         Button3,        toggletag,      {0} },
};

/* signal definitions */
/* signum must be greater than 0 */
/* trigger signals using `xsetroot -name "fsignal:<signum>"` */
static Signal signals[] = {
	/* signum       function        argument  */
	{ 9,            quit,      {.v = 0} },
/*	{ 70,           setlayout, {.v = 0} },
	{ 100,          view,      {.ui = 1 << -1} },
	{ 101,          view,       {.ui = 1 << 0} },
	{ 102,          view,       {.ui = 1 << 1} },
	{ 103,          view,       {.ui = 1 << 2} },
	{ 104,          view,       {.ui = 1 << 3} },
	{ 105,          view,       {.ui = 1 << 4} },
	{ 106,          view,       {.ui = 1 << 5} },
	{ 107,          view,       {.ui = 1 << 6} },
	{ 108,          view,       {.ui = 1 << 7} },
	{ 109,          view,       {.ui = 1 << 8} }, */
	{ 110,          runorraise,       {.v = filemanager} },
	{ 111,          runorraise,       {.v = termcmd} },
	{ 112,          runorraise,       {.v = firefox} },

};
