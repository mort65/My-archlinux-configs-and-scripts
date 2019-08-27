
# Tango theme for tty, the dark version.

if [ "$TERM" = "linux" ]; then
    echo -en "\e]PBfce94f" # S_base00
    echo -en "\e]PA8ae234" # S_base01
    echo -en "\e]P02e3436" # S_base02
    echo -en "\e]P607c7ca" # S_cyan
    echo -en "\e]P8888a85" # S_base03
    echo -en "\e]P24e9a06" # S_green
    echo -en "\e]P592659a" # S_magenta
    echo -en "\e]P1cc0000" # S_red
    echo -en "\e]PC729fcf" # S_base0
    echo -en "\e]PE63e9e9" # S_base1
    echo -en "\e]P9ef2929" # S_orange
    echo -en "\e]P7d3d7cf" # S_base2
    echo -en "\e]P43465a4" # S_blue
    echo -en "\e]P3edd400" # S_yellow
    echo -en "\e]PFeeeeec" # S_base3
    echo -en "\e]PDc19fbe" # S_violet
    clear # against bg artifacts
fi
