
# Gruvbox theme for tty, the light version.

if [ "$TERM" = "linux" ]; then
    echo -en "\e]PBb57614" # S_base00
    echo -en "\e]PA79740e" # S_base01
    echo -en "\e]P0fdf4c1" # S_base02
    echo -en "\e]P6689d6a" # S_cyan
    echo -en "\e]P8928374" # S_base03
    echo -en "\e]P298971a" # S_green
    echo -en "\e]P5b16286" # S_magenta
    echo -en "\e]P1cc241d" # S_red
    echo -en "\e]PC076678" # S_base0
    echo -en "\e]PE427b58" # S_base1
    echo -en "\e]P99d0006" # S_orange
    echo -en "\e]P77c6f64" # S_base2
    echo -en "\e]P4458588" # S_blue
    echo -en "\e]P3d79921" # S_yellow
    echo -en "\e]PF3c3836" # S_base3
    echo -en "\e]PD8f3f71" # S_violet
    clear # against bg artifacts
fi
