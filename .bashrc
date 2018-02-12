#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize


# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

#################################3
## File used for defining $PS1

bash_prompt_command() {
# How many characters of the $PWD should be kept
local pwdmaxlen=25
# Indicate that there has been dir truncation
local trunc_symbol=".."
local dir=${PWD##*/}
pwdmaxlen=$(( ( pwdmaxlen < ${#dir} ) ? ${#dir} : pwdmaxlen ))
NEW_PWD=${PWD/#$HOME/\~}
local pwdoffset=$(( ${#NEW_PWD} - pwdmaxlen ))
if [ ${pwdoffset} -gt "0" ]
then
    NEW_PWD=${NEW_PWD:$pwdoffset:$pwdmaxlen}
    NEW_PWD=${trunc_symbol}/${NEW_PWD#*/}
fi
}

bash_prompt() {
local NONE="\[\033[0m\]"    # unsets color to term's fg color

# regular colors
local K="\[\033[0;30m\]"    # black
local R="\[\033[0;31m\]"    # red
local G="\[\033[0;32m\]"    # green
local Y="\[\033[0;33m\]"    # yellow
local B="\[\033[0;34m\]"    # blue
local M="\[\033[0;35m\]"    # magenta
local C="\[\033[0;36m\]"    # cyan
local W="\[\033[0;37m\]"    # white

# empahsized (bolded) colors
local EMK="\[\033[1;30m\]"
local EMR="\[\033[1;31m\]"
local EMG="\[\033[1;32m\]"
local EMY="\[\033[1;33m\]"
local EMB="\[\033[1;34m\]"
local EMM="\[\033[1;35m\]"
local EMC="\[\033[1;36m\]"
local EMW="\[\033[1;37m\]"

# background colors
local BGK="\[\033[40m\]"
local BGR="\[\033[41m\]"
local BGG="\[\033[42m\]"
local BGY="\[\033[43m\]"
local BGB="\[\033[44m\]"
local BGM="\[\033[45m\]"
local BGC="\[\033[46m\]"
local BGW="\[\033[47m\]"

black=`tput setaf 0`
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
magenta=`tput setaf 5`
cyan=`tput setaf 6`
white=`tput setaf 7`
reset=`tput sgr0`

local UC=$W                 # user's color
[ $UID -eq "0" ] && UC=$R   # root's color

# without colors: PS1="[\u@\h \${NEW_PWD}]\\$ "
# extra backslash in front of \$ to make bash colorize the prompt

#returns exitcode of last command if it is not zero.
exitstatus()
{   
    local LASTEXIT=$?
    if [[ $LASTEXIT != 0 ]]; then
        tput setaf 1;echo $LASTEXIT
    else
	tput setaf 4;echo $LASTEXIT
    fi
    return
}

#Check for installation of jdate
jdatestatus()
{
 if [ -f /usr/bin/jdate ]; then
	echo "$(jdate '+%B %d')"
 fi
 return	
}



#Nat's Colored Prompt
if [ "$color_prompt" = yes ]; then
	PS1="${EMW}\n[${EMG}\d ${EMG}\@${EMW}][\$(exitstatus)${EMW}] \n${EMW} [${UC}\u${EMW}@${UC}\h ${EMB}\${NEW_PWD}${EMW}]\\$ ${NONE}"
else
	PS1='[\u@\h \W]\$ '
fi
unset color_prompt force_color_prompt 
#PS1="${EMW}\n[${EMG}\$(jdate '+%h %b %d %Y') ${EMW}]${EMW}\n[${EMG}\d ${EMG}\@${EMW}] \n${EMW} [${UC}\u${EMW}@${UC}\h ${EMB}\${NEW_PWD}${EMW}]${R}\$(exitstatus)${UC}\\$ ${NONE}"

#PS1="${EMW}\n[${EMG}\$(lsb_release -d) ${EMW}]${EMW}\n[${EMG}\d ${EMG}\@${EMW}] \n${EMW} [${UC}\u${EMW}@${UC}\h ${EMB}\${NEW_PWD}${EMW}]${R}\$(exitstatus)${UC}\\$ ${NONE}"


}
######################################

PROMPT_COMMAND=bash_prompt_command
bash_prompt
unset bash_prompt 

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'
 
# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi



#SFTP shorthand command
sftpin() {
	sftp 192.168.1."$1"
	return
}

export -f sftpin

#SSH shorthand command
sshin() {
	ssh 192.168.1."$1"
	return
}

export -f sshin

##Alias:
#####################################

alias c='clear'

# some more ls aliases
#alias ll='ls -l'
#alias la='ls -A'
#alias l='ls -CF'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

#force rm to ask before deleting every file:
alias del='rm -iv'

## get rid of command not found ##
alias cd..='cd ..'

## a quick way to get out of current directory ##
alias ..='cd ..' 
alias ...='cd ../../../' 
alias ....='cd ../../../../' 
alias .....='cd ../../../../' 
alias .4='cd ../../../../' 
alias .5='cd ../../../../..'

## Colorize the grep command output for ease of use (good for log files)##
#alias grep='grep --color=auto'
#alias egrep='egrep --color=auto'
#alias fgrep='fgrep --color=auto'

# Start calculator with math support
alias bc='bc -l'

# install  colordiff package :)
alias diff='colordiff'

# handy short cuts #
alias h='history'
alias j='jobs -l'

# Create a new set of commands
alias path='echo -e ${PATH//:/\\n}'
alias now='date +"%T"'
alias nowtime=now
alias nowdate='date +"%d-%m-%Y"'

# Set vim as default
alias vi=vim 
alias svi='sudo vi' 
alias vis='vim "+set si"' 
alias edit='vim'

# Stop after sending count ECHO_REQUEST packets #
alias ping='ping -c 5'
# Do not wait interval 1 second, go fast #
alias fastping='ping -c 100 -s.2'

# Show open ports
alias ports='netstat -tulanp'

#update system faster
alias yupdate='yaourt -Syyua'
alias pupdate='sudo pacman -Syyu'
alias update='yaourt -Syyua'

# reboot / halt / poweroff
alias reboot='sudo /sbin/reboot'
alias poweroff='sudo /sbin/poweroff'
alias halt='sudo /sbin/halt'
alias shutdown='sudo /sbin/shutdown'

## pass options to free ## 
alias meminfo='free -l -t -h'
 
## get top process eating memory
alias psmem='ps auxf | sort -nr -k 4'
alias psmem10='ps auxf | sort -nr -k 4 | head -10'
 
## get top process eating cpu ##
alias pscpu='ps auxf | sort -nr -k 3'
alias pscpu10='ps auxf | sort -nr -k 3 | head -10'
 
## Get server cpu info ##
alias cpuinfo='lscpu'
 
## older system use /proc/cpuinfo ##
##alias cpuinfo='less /proc/cpuinfo' ##

## get GPU ram on desktop / laptop## 
#alias gpumeminfo='grep -i --color memory /var/log/Xorg.0.log'

## this one saved by butt so many times ##
##Resume wget by default
alias wget='wget -c'

alias tfm="$HOME/bin/totalfreemem"
alias tfs="$HOME/bin/totalfreeswap"
alias tum="$HOME/bin/totalusedmem"
alias tus="$HOME/bin/totalusedswap"
alias tau="$HOME/bin/totalavailupdates"
alias up="$HOME/bin/update-arch"
alias upa="$HOME/bin/update-arch -sya"
alias upt="$HOME/bin/update-arch -t"
alias upta="$HOME/bin/update-arch -tsya"
alias upm="$HOME/bin/update-mirrors"
alias tf="$HOME/bin/totalfiles"
alias ver="/usr/bin/uname -r"
#alias mpv="/usr/bin/mpv --sub-scale=0.75 --volume-max=200"
 
# When using sudo, use alias expansion (otherwise sudo ignores your aliases)
alias sudo='/usr/bin/sudo '
#####################################

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi




##Env:
#####################################

export PATH=$PATH:$HOME/bin
export VISUAL="vim"
export EDITOR=vim

####################################


#bflogin.sh
archey3
#screenfetch
#echo "${cyan} $(jdate '+%h %d %B %Y %H:%M %p')"
