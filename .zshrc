# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=2000

# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename "/home/$(id -u -n)/.zshrc"

autoload -Uz compinit
compinit
# End of lines added by compinstall

setopt appendhistory autocd no_beep extendedglob nomatch notify hist_ignore_space hist_ignore_all_dups
bindkey -v

# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
ZSH=/usr/share/oh-my-zsh/

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
#ZSH_THEME="agnoster"
ZSH_THEME="rkj-custom"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
#HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git archlinux python sudo systemd web-search wd)


# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

ZSH_CACHE_DIR=$HOME/.oh-my-zsh-cache
if [[ ! -d $ZSH_CACHE_DIR ]]; then
  mkdir $ZSH_CACHE_DIR
fi

export DEFAULT_USER=$(id -u -n)
source $ZSH/oh-my-zsh.sh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

##Colors:
#####################################

Black=`/usr/bin/tput setaf 0`
Red=`/usr/bin/tput setaf 1`
Green=`/usr/bin/tput setaf 2`
Yellow=`/usr/bin/tput setaf 3`
Blue=`/usr/bin/tput setaf 4`
Magenta=`/usr/bin/tput setaf 5`
Cyan=`/usr/bin/tput setaf 6`
White=`/usr/bin/tput setaf 7`
Random=`/usr/bin/tput setaf $(/usr/bin/tr -cd '1-6' < /dev/urandom | /usr/bin/head -c 1; echo)`
Bold=`/usr/bin/tput bold 1`
Reset=`/usr/bin/tput sgr0`




##Functions:
#####################################

#add this directory to path
fpath=( ~/.zfuncs "${fpath[@]}" )
#mark the function in zfuncs to be automatically loaded upon its first reference
autoload -Uz syncit



#SFTP shorthand command
sftpin() {
	/usr/bin/sftp 192.168.1."$1"
	return
}

#export -f sftpin

#SSH shorthand command
sshin() {
	/usr/bin/ssh 192.168.1."$1"
	return
}

jdatestatus()
{
 if [ -s /usr/bin/jdate ]; then
	echo "$(/usr/bin/jdate '+%h %d %B %Y %H:%M %p')"
 else
    echo "$(/usr/bin/date '+%h %d %B %Y %H:%M %p')"
 fi
 return	
}


##Prompt
#####################################

#RPROMPT="[%F{yellow}%?%f][%F{green}%B$(date '+%a %b %e %H:%M')%f]"
#RPROMPT="[%F{green}%B$(jdatestatus)%f]"



##Alias:
#####################################

alias c='/usr/bin/clear'

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# ls, the common ones I use a lot shortened for rapid fire usage
alias l='ls -lFh'     #size,show type,human readable
alias la='ls -lAFh'   #long list,show almost all,show type,human readable
alias lr='ls -tRFh'   #sorted by date,recursive,show type,human readable
alias lt='ls -ltFh'   #long list,sorted by date,show type,human readable
alias ll='ls -l'      #long list
alias ldot='ls -ld .*'
alias lS='ls -1FSsh'
alias lart='ls -1Fcart'
alias lrt='ls -1Fcrt'

alias zshrc='$EDITOR ~/.zshrc' # Quick access to the ~/.zshrc file
alias notes='$EDITOR ~/.note/Arch_Notes.txt' 
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
#alias grep='/usr/bin/grep --color=auto'
#alias egrep='/usr/bin/egrep --color=auto'
#alias fgrep='/usr/bin/fgrep --color=auto'

# Start calculator with math support
alias bc='/usr/bin/bc -l'

# install  colordiff package :)
alias diff='/usr/bin/colordiff'

# handy short cuts #
alias h='history'
alias j='jobs -l'

# Create a new set of commands
alias path='echo -e ${PATH//:/\\n}'
alias now='/usr/bin/date +"%T"'
alias nowtime=now
alias nowdate='/usr/bin/date +"%d-%m-%Y"'

# Set vim as default
alias vi=vim 
alias svi='sudo vi' 
alias vis='/usr/bin/vim "+set si"' 
alias edit='/usr/bin/vim'

# Stop after sending count ECHO_REQUEST packets #
alias ping='/usr/bin/ping -c 5'
# Do not wait interval 1 second, go fast #
alias fastping='/usr/bin/ping -c 100 -s.2'

# Show open ports
alias ports='/usr/bin/netstat -tulanp'

#update system faster
alias yupdate='/usr/bin/yaourt -Syyua'
alias pupdate='/usr/bin/sudo pacman -Syyu'


# reboot / halt / poweroff
alias reboot='/usr/bin/sudo /sbin/reboot'
alias poweroff='/usr/bin/sudo /sbin/poweroff'
alias halt='/usr/bin/sudo /sbin/halt'
alias shutdown='/usr/bin/sudo /sbin/shutdown'

## pass options to free ## 
alias meminfo='/usr/bin/free -l -t -h'
 
## get top process eating memory
alias psmem='/usr/bin/ps auxf | sort -nr -k 4'
alias psmem10='/usr/bin/ps auxf | sort -nr -k 4 | head -10'
 
## get top process eating cpu ##
alias pscpu='/usr/bin/ps auxf | sort -nr -k 3'
alias pscpu10='/usr/bin/ps auxf | sort -nr -k 3 | head -10'
 
## Get server cpu info ##
alias cpuinfo='/usr/bin/lscpu'
 
## older system use /proc/cpuinfo ##
##alias cpuinfo='/usr/bin/less /proc/cpuinfo' ##

## get GPU ram on desktop / laptop## 
#alias gpumeminfo='/usr/bin/grep -i --color memory /var/log/Xorg.0.log'

## this one saved by butt so many times ##
##Resume wget by default
alias wget='/usr/bin/wget -c'


alias whereami='pwd' 


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
alias py="/usr/bin/python"
alias py3="/usr/bin/python3"
alias py2="/usr/bin/python2"
alias ver="/usr/bin/uname -r"
#alias mpv="/usr/bin/mpv --sub-scale=0.75 --volume-max=200"
 
# When using sudo, use alias expansion (otherwise sudo ignores your aliases)
alias sudo='/usr/bin/sudo '
 
##Env:
#####################################

export PATH=$PATH:$HOME/bin
export VISUAL="vim"
export EDITOR=vim

####################################
#archey3
#echo "${Bold}${Random}\n"
#~/bin/randcowsay
#~/bin/randsay.py
~/bin/randponysay
echo '\n'
echo "\t${Bold}${Random} $(jdatestatus)"
echo '\n'
neofetch

