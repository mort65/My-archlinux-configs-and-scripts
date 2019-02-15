/* See LICENSE file for copyright and license details. */

/* appearance */
static const unsigned int borderpx  = 1;        /* border pixel of windows */
static const unsigned int snap      = 32;       /* snap pixel */
static const unsigned int minwsz    = 20;       /* Minimal heigt of a client for smfact */
static const unsigned int gappx     = 6;        /* gap pixel between windows */
static const unsigned int systraypinning = 0;   /* 0: sloppy systray follows selected monitor, >0: pin systray to monitor X */
static const unsigned int systrayspacing = 2;   /* systray spacing */
static const int systraypinningfailfirst = 1;   /* 1: if pinning fails, display systray on the first monitor, False: display systray on the last monitor*/
static const int showsystray        = 1;     /* 0 means no systray */
static const int showbar            = 1;        /* 0 means no bar */
static const int topbar             = 1;        /* 0 means bottom bar */
static const char buttonbar[]       = "<O>";
static const char *fonts[]          = { "monospace:size=10" };
static const char dmenufont[]       = "monospace:size=10";
static const char col_gray1[]       = "#222222";
static const char col_gray2[]       = "#444444";
static const char col_gray3[]       = "#bbbbbb";
static const char col_gray4[]       = "#eeeeee";
static const char col_red[]         = "#ff0000";
static const char col_cyan[]        = "#005577";
static const char *colors[][6]      = {
	/*             fg       bg       border       float       sticky       permanent */
	[SchemeNorm] = { col_gray3, col_gray1, col_gray2, col_gray2, col_gray2, col_gray2 },
	[SchemeSel]  = { col_gray4, col_cyan,  col_cyan, col_cyan, col_cyan, col_cyan },
	[SchemeUrg] = { col_gray3, col_gray1, col_red, col_red, col_red, col_red },
};

/* tagging */
static const char *tags[] = { "1", "2", "3", "4", "5", "6", "7", "8", "9" };

static const Rule rules[] = {
	/* xprop(1):
	 *	WM_CLASS(STRING) = instance, class
	 *	WM_NAME(STRING) = title
	 */
	/* class      instance    title       tags mask     iscentered     isfloating   ispermanent    isterminal noswallow monitor */
	{ "Gimp",     NULL,       NULL,       0,            0,            1,           0,            0,         0,        -1 },
	{ "Firefox",  NULL,       NULL,       1 << 8,       0,            0,           0,            0,         0,        -1 },
	{ "st",       NULL,       NULL,       0,            0,            0,           0,            1,         1,        -1 },
};

/* layout(s) */
static const float mfact     = 0.55; /* factor of master area size [0.05..0.95] */
static const float smfact     = 0.00; /* factor of tiled clients [0.00..0.95] */
static const int nmaster     = 1;    /* number of clients in master area */
static const int resizehints = 1;    /* 1 means respect size hints in tiled resizals */

#include "fibonacci.c"
#include "gaplessgrid.c"
#include "horizgrid.c"
#include "layouts.c"
#include "tcl.c"
static const Layout layouts[] = {
	/* symbol     arrange function */
	{ "[]=",      tile },    /* first entry is default */
	{ "><>",      NULL },    /* no layout function means floating behavior */
	{ "[M]",      monocle },
	{ "|||",      col },
	{ "H^H",      tcl },
	{ "H[]",      deck },
	{ "TTT",      bstack },
	{ "===",      bstackhoriz },
	{ "HHH",      gaplessgrid },
	{ "###",      horizgrid },
 	{ "[@]",      spiral },
 	{ "[\\]",      dwindle },
	{ NULL,       NULL },
};

/* key definitions */
#define MODKEY Mod1Mask
#define TAGKEYS(KEY,TAG) \
	{ KeyPress,   MODKEY,                       KEY,      view,           {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ControlMask,           KEY,      toggleview,     {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ShiftMask,             KEY,      tag,            {.ui = 1 << TAG} }, \
	{ KeyPress,   MODKEY|ControlMask|ShiftMask, KEY,      toggletag,      {.ui = 1 << TAG} },

/* helper for spawning shell commands in the pre dwm-5.0 fashion */
#define SHCMD(cmd) { .v = (const char*[]){ "/bin/sh", "-c", cmd, NULL } }

/* commands */
static char dmenumon[2] = "0"; /* component of dmenucmd, manipulated in spawn() */
static const char *dmenucmd[] = { "dmenu_run", "-m", dmenumon, "-fn", dmenufont, "-nb", col_gray1, "-nf", col_gray3, "-sb", col_cyan, "-sf", col_gray4, NULL };
static const char *termcmd[]  = { "st", NULL };
static const char scratchpadname[] = "scratchpad";
static const char *scratchpadcmd[] = { "st", "-t", scratchpadname, "-g", "120x34", NULL };

#include "selfrestart.c"
#include "shiftview.c"
#include "zoomswap.c"

static Key keys[] = {
/*        type          modifier                      key        function        argument */
	{ KeyPress,	MODKEY,                       33,      spawn,          {.v = dmenucmd } }, // p
	{ KeyPress,	MODKEY|ShiftMask,             36, spawn,          {.v = termcmd } }, // Return
        { MODKEY,                                     49,  togglescratch,  {.v = scratchpadcmd } }, // ` Grave
	{ KeyPress,	MODKEY,                       56,      togglebar,      {0} }, // b
	{ KeyPress,	MODKEY|ShiftMask,             44,      rotatestack,    {.i = +1 } }, // j
	{ KeyPress,	MODKEY|ShiftMask,             45,      rotatestack,    {.i = -1 } }, // k
	{ KeyPress,	MODKEY,                       44,      focusstack,     {.i = +1 } }, // j
	{ KeyPress,	MODKEY,                       45,      focusstack,     {.i = -1 } }, // k
	{ KeyPress,	MODKEY,                       31,      incnmaster,     {.i = +1 } }, // i
	{ KeyPress,	MODKEY,                       40,      incnmaster,     {.i = -1 } }, // d
        { KeyPress,	MODKEY|ShiftMask,             31,      shiftview,  { .i = +1 } }, // i
        { KeyPress,	MODKEY|ShiftMask,             30,      shiftview,  { .i = -1 } }, // u
	{ KeyPress,	MODKEY,                       43,      setmfact,       {.f = -0.05} }, // h
	{ KeyPress,	MODKEY,                       46,      setmfact,       {.f = +0.05} }, // l
	{ KeyPress,	MODKEY|ShiftMask,             43,      setsmfact,      {.f = +0.05} }, // l
	{ KeyPress,	MODKEY|ShiftMask,             43,      setsmfact,      {.f = -0.05} }, // l
	{ KeyPress,	MODKEY,                       36,        zoom,           {0} }, // Return
	{ KeyPress,	MODKEY,                       23,        view,           {0} }, // Tab
	{ KeyPress,	MODKEY|ShiftMask,             54,      killclient,     {0} }, // c
	{ KeyPress,     MODKEY|ShiftMask,             53,      killunsel,      {0} }, // x
	{ KeyPress,	MODKEY,                       28,      setlayout,      {.v = &layouts[0]} }, // t
	{ KeyPress,	MODKEY,                       41,      setlayout,      {.v = &layouts[1]} }, //f
	{ KeyPress,	MODKEY,                       58,      setlayout,      {.v = &layouts[2]} }, // m
	{ KeyPress,	MODKEY|ControlMask,	      59,      cyclelayout,    {.i = -1 } }, // Comma
	{ KeyPress,	MODKEY|ControlMask,           60, cyclelayout,    {.i = +1 } }, // Period
	{ KeyPress,	MODKEY,                       65,  setlayout,      {0} }, // Space
	{ KeyPress,	MODKEY|ShiftMask,             65,  togglefloating, {0} }, // space
	{ KeyPress,	MODKEY,                       57,      togglesticky,   {0} }, // n
	{ KeyPress,	MODKEY,                       19,      view,           {.ui = ~0 } }, // 0
	{ KeyPress,	MODKEY|ShiftMask,             19,      tag,            {.ui = ~0 } }, // 0
	{ KeyPress,	MODKEY,                       59,  focusmon,       {.i = -1 } }, // Comma
	{ KeyPress,	MODKEY,                       60, focusmon,       {.i = +1 } }, // Period
	{ KeyPress,	MODKEY|ShiftMask,             59,  tagmon,         {.i = -1 } }, // Comma
	{ KeyPress,	MODKEY|ShiftMask,             60, tagmon,         {.i = +1 } }, // Period
	TAGKEYS(                        10,                      0) // 1
	TAGKEYS(                        11,                      1) // 2
	TAGKEYS(                        12,                      2) // 3
	TAGKEYS(                        13,                      3) // 4
	TAGKEYS(                        14,                      4) // 5
	TAGKEYS(                        15,                      5) // 6
	TAGKEYS(                        16,                      6) // 7
	TAGKEYS(                        17,                      7) // 8
	TAGKEYS(                        18,                      8) // 9
    { KeyPress,	MODKEY|ShiftMask,       27,      self_restart,   {0} }, // r
	{ KeyPress,	MODKEY|ShiftMask,             24,      quit,           {0} }, // q
	{ KeyPress,	MODKEY|ControlMask|ShiftMask, 24,      quit,           {1} }, // q
};

/* button definitions */
/* click can be ClkTagBar, ClkLtSymbol, ClkStatusText, ClkWinTitle, ClkClientWin, or ClkRootWin */
static Button buttons[] = {
	/* click                event mask      button          function        argument */
	{ ClkButton,		0,		Button1,	spawn,		{.v = dmenucmd } },
	{ ClkLtSymbol,          0,              Button1,        setlayout,      {0} },
	{ ClkLtSymbol,          0,              Button3,        setlayout,      {.v = &layouts[2]} },
	{ ClkStatusText,        0,              Button2,        spawn,          {.v = termcmd } },
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
	{ 1,            setlayout,      {.v = 0} },
};
