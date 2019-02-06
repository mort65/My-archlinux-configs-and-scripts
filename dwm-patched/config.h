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
static const char buttonbar[]       = "⮞";
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
	/*Match condition   Tags   Float   Permanent   Terminal   Swallow   Monitor*/
	{ CLASS("Firefox|Chromium|Google-chrome|Vivaldi-stable"),   TAG(2),   0,   0,   0 },
        { CLASS("VirtualBox"),   TAG(5),   0,   0 },
        { CLASS("St|UXTerm|XTerm|rxvt|URxvt|Urxvt-tabbed|Lxterminal"),   TAG(1),   0,   0,   1,   1,   0 },
        { CLASS("Thunar|Pcmanfm|pcmanfm-qt"),   TAG(3),   0,   0 },
	{ CLASS("vlc|smplayer|mpv|smplayer"),   TAG(1)|TAG(3)|TAG(4),   0,   0,   0,   0 },
	{ CLASS("Steam"),  TAG(6) ,   0,   0 },

        /*Floating windows*/
	{ CLASS("Nitrogen|Dukto|Galculator|lxsu|lxsudo|Gpick"),   0,   1,   0,   0,   0 },
	{ CLASS("Pragha"),  TAG(4) ,   1,   0 },
        { TITLE("File Operation Progress"),   0,   1,   0,   0 },
        { TITLE("Module"),   0,   1,   0 },
        { TITLE("Search Dialog"),   0,   1,   0,   0 },
        { TITLE("Goto"),   0,   1,   0,   0 },
        { TITLE("IDLE Preferences"),   0,   1,   0,   0 },
        { TITLE("Preferences"),   0,   1,   0,   0 },
        { TITLE("File Transfer"),   0,   1,   0,   0 },
        { TITLE("branchdialog"),   0,   1,   0,   0 },
        { TITLE("pinentry"),   0,   1,   0,   0 },
        { TITLE("confirm"),   0,   1,   0,   0 },
        { INSTANCE("eog"),   0,   1,    0,   0 },
	{ CLASS_W_TITLE("Firefox","Firefox Preferences"),   TAG(2),   1,   0,   0 },
	{ CLASS_W_TITLE("Firefox","Library"),   TAG(2),   1,   0,   0 },
};

/* layout(s) */
static const float mfact     = 0.55; /* factor of master area size [0.05..0.95] */
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
    spiral_layout,
    dwindle_layout,
};

#include "fibonacci.c"
#include "gaplessgrid.c"
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
 	[spiral_layout]   = { "[@]",      spiral },
 	[dwindle_layout]  = { "[\\]",      dwindle },
	                    { NULL,       NULL },
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

/* key definitions */
#define MODKEY Mod4Mask
#define ALTMODKEY Mod1Mask
#define TAGKEYS(KEY,TAG) \
	{ KeyPress,   MODKEY,                       KEY,      view,           {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ControlMask,           KEY,      toggletag,     {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ShiftMask,             KEY,      tag,            {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ALTMODKEY,             KEY,      toggleview,      {.ui = 1 << TAG} },

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
static const char *firefox[] = { "firefox", NULL, NULL, NULL, "Firefox", "2", NULL};
static const char *filemanager[] = { "pcmanfm", NULL, NULL, NULL, "Pcmanfm", "3", NULL};
static const char *ranger[] = { "urxvt", "-e", "ranger" };
static const char *nnn[] = { "st", "-e", "nnnstart" };
static const char *cmus[] = { "st", "-e", "cmus" };
static const char *musicplayer[] = { "pragha", NULL, NULL, NULL, "Pragha", "4", NULL};
static const char *texteditor[] = { "geany", NULL, NULL, NULL, "Geany", NULL, NULL };
static const char *volumeup[] = { "amixer", "set", "Master", "5%+", NULL };
static const char *volumedown[] = { "amixer", "set", "Master", "5%-", NULL };
static const char *volumemute[] = { "amixer", "set", "Master", "toggle", NULL };
static const char *audionext[] = { "playerctl", "next", NULL };
static const char *audioprev[] = { "playerctl", "previous", NULL };
static const char *audiostop[] = { "playerctl", "stop" };
static const char *lock[] = { "slock", NULL };
static const char *lxtask[] = { "lxtask", NULL, NULL, NULL, "Lxtask", NULL, NULL };
static const char *htop[] = { "st", "-e", "htop", NULL };

#include "selfrestart.c"
#include "moveresize.c"
#include "shiftview.c"
#include "zoomswap.c"

static Key keys[] = {
/*	 type            modifier                     key        function        argument */
	{KeyPress,	 MODKEY,                       XK_o,      spawn,          {.v = dmenucmd } },
	{ KeyPress,	 MODKEY,                       XK_p,      spawn,          {.v = roficmd } },
	{ KeyPress,	 MODKEY|ControlMask,           XK_Return, runorraise,          {.v = termcmd } },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_Return, runorraise,          {.v = termcmd1 } },
	{ KeyPress,	 MODKEY|ALTMODKEY,             XK_Return, runorraise,          {.v = termcmd2 } },
        { KeyPress,	 MODKEY,                       XK_grave,  togglescratch,  {.v = scratchpadcmd } },
	{ KeyPress,	 MODKEY,                       XK_b,      togglebar,      {0} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_b,      spawn,          SHCMD("~/.script/dwm-toggle_dzen") },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_j,      rotatestack,    {.i = +1 } },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_k,      rotatestack,    {.i = -1 } },
	{ KeyPress,	 MODKEY,                       XK_j,      focusstack,     {.i = +1 } },
	{ KeyPress,	 MODKEY,                       XK_k,      focusstack,     {.i = -1 } },
	{ KeyPress,	 MODKEY,                       XK_i,      incnmaster,     {.i = +1 } },
	{ KeyPress,	 MODKEY,                       XK_d,      incnmaster,     {.i = -1 } },
        { KeyPress,	 MODKEY|ShiftMask,             XK_i,      shiftview,      {.i = +1 } },
        { KeyPress,	 MODKEY|ShiftMask,             XK_u,      shiftview,      {.i = -1 } },
        { KeyPress,	 MODKEY,                       XK_h,      setmfact,       {.f = -0.05} },
	{ KeyPress,	 MODKEY,                       XK_l,      setmfact,       {.f = +0.05} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_h,      setsmfact,      {.f = +0.05} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_l,      setsmfact,      {.f = -0.05} },
	{ KeyPress,	 MODKEY,                       XK_Return, zoom,           {0} },
	{ KeyPress,	 MODKEY,                       XK_Tab,    view,           {0} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_c,      killclient,     {0} },
	{ KeyPress,	 MODKEY,                       XK_t,      setlayout,      {.v = &layouts[0]} },
	{ KeyPress,	 MODKEY,                       XK_f,      setlayout,      {.v = &layouts[1]} },
	{ KeyPress,	 MODKEY,                       XK_m,      setlayout,      {.v = &layouts[2]} },
	{ KeyPress,	 MODKEY,                       XK_c,      setlayout,      {.v = &layouts[3]} },
	{ KeyPress,	 MODKEY,                       XK_e,      setlayout,      {.v = &layouts[4]} },
	{ KeyPress,	 MODKEY,                       XK_v,      setlayout,      {.v = &layouts[5]} },
	{ KeyPress,	 MODKEY,                       XK_y,      setlayout,      {.v = &layouts[6]} },
	{ KeyPress,	 MODKEY,                       XK_u,      setlayout,      {.v = &layouts[7]} },
	{ KeyPress,	 MODKEY,                       XK_g,      setlayout,      {.v = &layouts[8]} },
	{ KeyPress,	 MODKEY,                       XK_s,      setlayout,      {.v = &layouts[9]} },
	{ KeyPress,	 MODKEY,                       XK_w,      setlayout,      {.v = &layouts[10]} },
	{ KeyPress,	 MODKEY,		        XK_comma,  cyclelayout,    {.i = -1 } },
	{ KeyPress,	 MODKEY,                       XK_period, cyclelayout,    {.i = +1 } },
	{ KeyPress,	 MODKEY,                       XK_space,  setlayout,      {0} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_space,  togglefloating, {0} },
	{ KeyPress,	 MODKEY,                       XK_n,      togglesticky,   {0} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_n,      togglepermanent,{0} },
	{ KeyPress,	 MODKEY,                       XK_0,      view,           {.ui = ~0 } },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_0,      tag,            {.ui = ~0 } },
	{ KeyPress,	 MODKEY|ALTMODKEY,             XK_comma,  focusmon,       {.i = -1 } },
	{ KeyPress,	 MODKEY|ALTMODKEY,             XK_period, focusmon,       {.i = +1 } },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_comma,  tagmon,         {.i = -1 } },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_period, tagmon,         {.i = +1 } },
	{ KeyPress,	 MODKEY,                       XK_bracketleft,   togglemark,     {0} },
	{ KeyPress,	 MODKEY,                       XK_bracketright,  swapfocus,     {0} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_bracketright,  swapclient,      {0} },
	{ KeyPress,	 Mod4Mask,						XK_Up,						moveresize,			{.v = "0x -25y 0w 0h"} },
	{ KeyPress,	 MODKEY,						XK_Down,					moveresize,			{.v = "0x 25y 0w 0h"} },
	{ KeyPress,	 MODKEY,						XK_Left,					moveresize,			{.v = "-25x 0y 0w 0h"} },
	{ KeyPress,	 MODKEY,						XK_Right,					moveresize,			{.v = "25x 0y 0w 0h"} },
	{ KeyPress,	 MODKEY|ShiftMask,			XK_Up,						moveresize,			{.v = "0x 0y 0w -25h"} },
	{ KeyPress,	 MODKEY|ShiftMask,			XK_Down,					moveresize,			{.v = "0x 0y 0w 25h"} },
	{ KeyPress,	 MODKEY|ShiftMask,			XK_Left,					moveresize,			{.v = "0x 0y -25w 0h"} },
	{ KeyPress,	 MODKEY|ShiftMask,			XK_Right,					moveresize,			{.v = "0x 0y 25w 0h"} },
	TAGKEYS(                        XK_1,                      0)
	TAGKEYS(                        XK_2,                      1)
	TAGKEYS(                        XK_3,                      2)
	TAGKEYS(                        XK_4,                      3)
	TAGKEYS(                        XK_5,                      4)
	TAGKEYS(                        XK_6,                      5)
	TAGKEYS(                        XK_7,                      6)
	TAGKEYS(                        XK_8,                      7)
	TAGKEYS(                        XK_9,                      8)
        { KeyPress,	 MODKEY|ShiftMask,             XK_r,      self_restart,   {0} },
	/*{ KeyPress,	 MODKEY|ShiftMask,             XK_q,      quit,           {0} },*/
	{ KeyPress,	 MODKEY|ControlMask|ShiftMask, XK_q,      quit,           {1} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_Scroll_Lock,      spawn,           {.v = lock} },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_q,      spawn,          SHCMD("~/.script/dwm-logout_menu") },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_Pause,  spawn,          SHCMD("~/.script/dwm-rofi_runit_exit_menu") },
	{ KeyPress,	 MODKEY|ShiftMask,             XK_x,      spawn,          SHCMD("xkill") },
	{ KeyPress,	 MODKEY|ControlMask,           XK_r,      spawn,          {.v = ranger} },
	{ KeyPress,	 MODKEY|ControlMask,           XK_n,      spawn,          {.v = nnn} },
	{ KeyPress,	 MODKEY|ControlMask,           XK_m,      spawn,          {.v = cmus} },
	{ KeyPress,	 MODKEY|ControlMask,           XK_p,      runorraise,     {.v = musicplayer} },
	{ KeyPress,	 0,       XF86XK_AudioRaiseVolume,        spawn,          {.v = volumeup} },
	{ KeyPress,	 0,       XF86XK_AudioLowerVolume,        spawn,          {.v = volumedown} },
	{ KeyPress,	 0,       XF86XK_AudioMute,               spawn,          {.v = volumemute} },
	{ KeyPress,	 0,       XF86XK_AudioNext,               spawn,          {.v = audionext} },
	{ KeyPress,	 0,       XF86XK_AudioPrev,               spawn,          {.v = audioprev} },
	{ KeyPress,	 0,       XF86XK_AudioStop,               spawn,          {.v = audiostop} },
        { KeyPress,	 MODKEY|ControlMask,           XK_w,      runorraise,     {.v = firefox} },
        { KeyPress,	 MODKEY|ControlMask,           XK_Home,   runorraise,     {.v = filemanager} },
        { KeyPress,	 MODKEY|ControlMask,           XK_e,      runorraise,     {.v = texteditor} },
        { KeyPress,	 MODKEY|ControlMask,           XK_Delete, runorraise,     {.v = lxtask} },
        { KeyPress,	 MODKEY,                       XK_Delete, spawn,          {.v = htop} },
        { KeyPress,	 MODKEY,	               XK_F1,     spawn,          SHCMD("jgmenu_run") },
        { KeyPress,	 MODKEY,	               XK_F2,     spawn,          SHCMD("~/.script/dwm-app_menu") },
	{ KeyPress,	 MODKEY,	               XK_F3,     spawn,          SHCMD("gksudo") },
        { KeyRelease,	 MODKEY,                       XK_Print,  spawn,          SHCMD("~/bin/winshot") },
        { KeyRelease,	 0,                            XK_Print,  spawn,          SHCMD("~/bin/screenshot") },


};

/* button definitions */
/* click can be ClkTagBar, ClkLtSymbol, ClkStatusText, ClkWinTitle, ClkClientWin, or ClkRootWin */
static Button buttons[] = {
	/* click                event mask      button          function        argument */
	/* { ClkButton,		0,		Button1,	spawn,		SHCMD("~/.script/dwm-app_menu") }, */
	{ ClkButton,		0,		Button1,	spawn,		SHCMD("jgmenu_run") },
	{ ClkButton,		0,		Button2,	spawn,		SHCMD("jgmenu_run") },
	{ ClkButton,		0,		Button3,	spawn,		SHCMD("~/.script/dwm-app_menu") },
	{ ClkLtSymbol,          0,              Button1,        setlayout,      {0} },
	{ ClkLtSymbol,          0,              Button3,        setlayout,      {.v = &layouts[2]} },
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
