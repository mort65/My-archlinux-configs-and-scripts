# Gruvbox theme for tty, the dark version.

if [ "$TERM" = "linux" ]; then
    echo -en "\e]PBfabd2f" # S_base00
    echo -en "\e]PAb8bb26" # S_base01
    echo -en "\e]P0282828" # S_base02
    echo -en "\e]P6689d6a" # S_cyan
    echo -en "\e]P8928374" # S_base03
    echo -en "\e]P298971a" # S_green
    echo -en "\e]P5b16286" # S_magenta
    echo -en "\e]P1cc241d" # S_red
    echo -en "\e]PC83a598" # S_base0
    echo -en "\e]PE8ec07c" # S_base1
    echo -en "\e]P9fb4934" # S_orange
    echo -en "\e]P7a89984" # S_base2
    echo -en "\e]P4458588" # S_blue
    echo -en "\e]P3d79921" # S_yellow
    echo -en "\e]PFebdbb2" # S_base3
    echo -en "\e]PDd3869b" # S_violet
    clear # against bg artifacts
fi
